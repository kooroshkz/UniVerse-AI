from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
import subprocess
from django.conf import settings
from .models import StaffMember
from .utils import search_staff
from openai import OpenAI

# Configure OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def chatbot_response(request):
    """
    Handles chatbot queries with dynamic database integration and OpenAI fallback.
    """
    user_input = request.POST.get('message')
    response_message = ""
    use_openai = True

    try:
        # Search for staff in the database
        staff = search_staff(user_input)

        if staff:
            # Construct direct responses for database-related queries
            if "email" in user_input.lower():
                response_message = f"The email address of {staff.name} is {staff.email}."
                use_openai = False
            elif "room number" in user_input.lower() or "room" in user_input.lower():
                response_message = f"{staff.name}'s room number is {staff.address}."
                use_openai = False
            elif "phone" in user_input.lower():
                response_message = f"The phone number of {staff.name} is {staff.phone}."
                use_openai = False
            elif "role" in user_input.lower():
                response_message = f"{staff.name}'s role is {staff.role}."
                use_openai = False
            else:
                # Generic response with all details
                response_message = (
                    f"Name: {staff.name}, Role: {staff.role}, "
                    f"Email: {staff.email}, Phone: {staff.phone}, "
                    f"Room: {staff.address}."
                )
                use_openai = False

        if use_openai:
            # Query OpenAI for general knowledge
            database_context = (
                f"Name: {staff.name}, Role: {staff.role}, Email: {staff.email}, "
                f"Phone: {staff.phone}, Address: {staff.address}."
                if staff else "No relevant data found."
            )

            prompt = (
                f"You are a helpful assistant for Leiden University. "
                f"If a question relates to university staff, refer to the following database context: {database_context}. "
                f"Otherwise, answer based on general knowledge. "
                f"User query: {user_input}"
            )

            openai_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful university assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

            response_message = openai_response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        response_message = "Sorry, I'm having trouble processing your request at the moment."

    return JsonResponse({"response": response_message})


def chatbot_view(request):
    """
    Renders the chatbot UI.
    """
    return render(request, 'chatbot/index.html')
