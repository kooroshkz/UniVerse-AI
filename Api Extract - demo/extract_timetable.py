import requests
from icalendar import Calendar
import csv
import re
from datetime import datetime
import pytz

# URL for fetching calendar data
url = "https://rooster.universiteitleiden.nl/ical?671f8c3b&eu=czQwNjg4NTg=&h=hbyDGcGHlQoU7WHVVuPYNMdizZF6gOU1bJqYeVdjOgs="

# Fetch the calendar data
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the timetable data. Status code: {response.status_code}")
    exit()

# Parse the iCalendar data
calendar = Calendar.from_ical(response.content)

# Prepare to write to CSV
with open('timetable.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Course_name', 'Course_Type', 'Start_time', 'End_time', 'Locations', 'Staffs'])

    # Parse each event in the calendar
    for component in calendar.walk():
        if component.name == "VEVENT":
            # Extract fields
            summary = component.get('summary')
            start = component.get('dtstart').dt
            end = component.get('dtend').dt
            description = component.get('description', '')
            location = component.get('location', '')
            
            # Convert start and end times to CET
            cet_timezone = pytz.timezone("CET")
            start_cet = start.astimezone(cet_timezone) if start.tzinfo else cet_timezone.localize(start)
            end_cet = end.astimezone(cet_timezone) if end.tzinfo else cet_timezone.localize(end)

            # Extract information using regex and parsing logic
            course_name = summary.split(' - ')[1] if ' - ' in summary else summary
            course_type_match = re.search(r"Type: (\w+)", description)
            course_type = course_type_match.group(1) if course_type_match else "Unknown"

            # Handle multiple locations and staff members
            locations = ', '.join(re.findall(r"Location\(s\):(.+?)Staff", description, re.DOTALL)).strip().replace("\n", ", ")
            staff_members = ', '.join(re.findall(r"Staff member\(s\):(.+?)Class", description, re.DOTALL)).strip().replace("\n", ", ")

            # Write each event to CSV
            writer.writerow([
                course_name,
                course_type,
                start_cet.strftime("%Y-%m-%d %H:%M:%S"),
                end_cet.strftime("%Y-%m-%d %H:%M:%S"),
                locations,
                staff_members
            ])

print("Timetable data has been written to 'timetable.csv'.")
