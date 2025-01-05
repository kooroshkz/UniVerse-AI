from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone, timedelta
from .utils import search_staff, search_course
from .models import CourseSchedule
import tiktoken
from django.conf import settings
from fuzzywuzzy import process
from django.db.models import Q
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar
import json
import pytz
import logging
import re

logger = logging.getLogger(__name__)

# Constants
MAX_INPUT_TOKENS = 20
MAX_OUTPUT_TOKENS = 200

# Helper Functions
def count_tokens(text):
    """Counts tokens in the text using the tiktoken library."""
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    return len(tokens)

def get_current_cet_time():
    """Gets the current Central European Time (CET)."""
    cet = timezone(timedelta(hours=1))
    return datetime.now(cet).strftime('%Y-%m-%d %H:%M:%S')

def validate_google_api():
    """Validates the Google API Key and Custom Search Engine (CX)."""
    api_key = getattr(settings, 'GOOGLE_API_KEY', None)
    cx = getattr(settings, 'GOOGLE_CX', None)

    if not api_key or not cx:
        logger.error("GOOGLE_API_KEY or GOOGLE_CX is not configured in settings.")
        return False

    test_query = "Leiden University"
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": test_query,
    }
    try:
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            logger.info("Google API credentials are valid.")
            return True
        else:
            logger.error(f"Google API returned status code {response.status_code}. Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Exception during API validation: {e}")
        return False

# Add Timetable
@csrf_exempt
def add_timetable(request):
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            timetable_url = data.get("link")
            print("Received URL:", timetable_url)  # Debug

            if not timetable_url:
                return JsonResponse({"error": "No URL provided."}, status=400)

            # Fetch the .ics file content
            response = requests.get(timetable_url)
            print("Fetch Status:", response.status_code)  # Debug
            if response.status_code != 200:
                return JsonResponse({"error": "Unable to fetch timetable."}, status=400)

            ics_data = response.text

            # Parse the .ics content
            calendar = Calendar.from_ical(ics_data)
            cet_timezone = pytz.timezone("CET")

            for component in calendar.walk():
                if component.name == "VEVENT":
                    # Extract fields
                    summary = component.get('SUMMARY', 'No summary available')
                    start = component.get('DTSTART').dt
                    end = component.get('DTEND').dt
                    description = component.get('DESCRIPTION', '')
                    location = component.get('LOCATION', 'Unknown location')

                    # Convert start and end times to CET
                    start_cet = start.astimezone(cet_timezone) if start.tzinfo else cet_timezone.localize(start)
                    end_cet = end.astimezone(cet_timezone) if end.tzinfo else cet_timezone.localize(end)

                    # Extract information using regex and parsing logic
                    course_name = summary.split(' - ')[1] if ' - ' in summary else summary
                    course_type_match = re.search(r"Type: (\w+)", description)
                    course_type = course_type_match.group(1) if course_type_match else "Lecture"

                    # Handle multiple locations and staff members
                    locations = ', '.join(re.findall(r"Location\(s\):(.+?)Staff", description, re.DOTALL)).strip().replace("\n", ", ") or location
                    staff_members = ', '.join(re.findall(r"Staff member\(s\):(.+?)Class", description, re.DOTALL)).strip().replace("\n", ", ")

                    print("Parsed Event:", course_name, course_type, start_cet, end_cet, locations, staff_members)  # Debug

                    # Save the event to the database
                    CourseSchedule.objects.create(
                        course_name=course_name,
                        course_type=course_type,
                        start_time=start_cet,
                        end_time=end_cet,
                        locations=locations,
                        staffs=staff_members
                    )

            return JsonResponse({"success": "Timetable added successfully!"})
        except Exception as e:
            print(f"Error in add_timetable: {str(e)}")  # Debug
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

def google_search(query):
    """
    Performs a Google search using the Google Custom Search JSON API.
    Fetch and scrape detailed data from the top result links, extracting only textual content.
    """
    if not validate_google_api():
        return [{"error": "Invalid Google API credentials."}]

    API_KEY = settings.GOOGLE_API_KEY
    CX = settings.GOOGLE_CX
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
    }
    response = requests.get(search_url, params=params)
    detailed_results = []

    if response.status_code == 200:
        results = response.json().get('items', [])
        for item in results[:3]:  # Limit to top 3 results
            # Extract title, link, and snippet with default values to avoid KeyError
            title = item.get('title', 'No title available')
            link = item.get('link', 'No link available')
            snippet = item.get('snippet', 'No snippet available')

            # Attempt detailed content scraping
            detailed_text = "No additional details available."
            try:
                page_response = requests.get(link, timeout=5)  # Added timeout to prevent hanging
                if page_response.status_code == 200:
                    soup = BeautifulSoup(page_response.text, 'html.parser')
                    main_content = soup.find('main') or soup.find('body')
                    if main_content:
                        # Remove script and style tags
                        for script_or_style in main_content(['script', 'style']):
                            script_or_style.decompose()

                        # Extract clean text from the main content
                        detailed_text = main_content.get_text(separator="\n", strip=True)

                        # Limit the amount of text to avoid overwhelming the OpenAI API
                        detailed_text = detailed_text[:2000]  # Limit to the first 2000 characters
                else:
                    detailed_text = "Failed to fetch detailed page content."
            except Exception as e:
                detailed_text = f"Error fetching details: {e}"

            # Append all extracted information to the results list
            detailed_results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "details": detailed_text
            })
    else:
        detailed_results.append({"error": f"Google API returned status code {response.status_code}."})

    return detailed_results

# Chatbot Response
@csrf_exempt
def chatbot_response(request):
    """
    Handles chatbot responses with enhanced fuzzy search for courses and staff.
    """
    user_input = request.POST.get('message', '')
    response_message = ""
    context_data = ""
    use_openai = True

    # Check token limit
    user_input_tokens = count_tokens(user_input)
    if user_input_tokens > MAX_INPUT_TOKENS:
        return JsonResponse({
            "error": "Input exceeds maximum token limit.",
            "max_tokens": MAX_INPUT_TOKENS,
            "user_input_tokens": user_input_tokens
        })

    try:
        # Add current CET time to the context
        context_data += f"Current CET Time: {get_current_cet_time()}\n"

        # Check for course-related information
        course = search_course(user_input)
        if course:
            context_data += (
                f"Course: {course.course_name}, Type: {course.course_type}, Start: {course.start_time}, "
                f"End: {course.end_time}, Location: {course.locations}, Staffs: {course.staffs}.\n"
            )

        # Check for staff-related information
        staff = search_staff(user_input)
        if staff:
            context_data += (
                f"Staff: Name: {staff.name}, Role: {staff.role}, Email: {staff.email}, "
                f"Phone: {staff.phone}, Address: {staff.address}.\n"
            )

        # Use Google Search API for other queries
        if not course and not staff:
            google_results = google_search(user_input)
            if google_results:
                context_data += "Google Search Results:\n"
                for item in google_results:
                    # Ensure graceful handling of missing keys
                    title = item.get('title', 'No title available')
                    link = item.get('link', 'No link available')
                    snippet = item.get('snippet', 'No snippet available')
                    details = item.get('details', 'No details available')

                    context_data += (
                        f"Title: {title}\n"
                        f"Link: {link}\n"
                        f"Snippet: {snippet}\n"
                        f"Details: {details}\n\n"
                    )

        # Generate a response using OpenAI
        if use_openai:
            openai_prompt = (
                f"You are a virtual assistant for Leiden University. Provide accurate, helpful, and concise information.\n"
                f"Context:\n{context_data if context_data else 'No relevant context available.'}\n"
                f"User Query: {user_input}\n"
            )

            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY_LEIDEN)
                openai_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful university assistant."},
                        {"role": "user", "content": openai_prompt}
                    ],
                    max_tokens=MAX_OUTPUT_TOKENS
                )
                response_message = openai_response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI error: {e}")
                response_message = f"I'm sorry, I couldn't fetch the response. Error: {e}."
    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        response_message = "Sorry, I'm having trouble processing your request at the moment."

    return JsonResponse({"response": response_message})

def chatbot_view(request):
    first_message = request.GET.get('first_message', '')
    return render(request, 'chatbot/index.html', {'first_message': first_message})

@csrf_exempt
def validate_tokens(request):
    """
    Checks the token count of the given input and returns whether it exceeds the limit.
    """
    user_input = request.POST.get('message', '')
    token_count = count_tokens(user_input)
    return JsonResponse({
        "token_count": token_count,
        "exceeds_limit": token_count > MAX_INPUT_TOKENS,
        "max_tokens": MAX_INPUT_TOKENS,
    })
