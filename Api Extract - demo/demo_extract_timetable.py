import requests
from icalendar import Calendar


url = "https://rooster.universiteitleiden.nl/ical?671f8c3b&eu=czQwNjg4NTg=&h=hbyDGcGHlQoU7WHVVuPYNMdizZF6gOU1bJqYeVdjOgs="


response = requests.get(url)


if response.status_code == 200:
    # Parse the iCalendar data
    calendar = Calendar.from_ical(response.content)

    timetable_events = []

    # Iterate through the events in the calendar
    for component in calendar.walk():
        if component.name == "VEVENT":
            description = component.get('description', '')
            description_lines = description.splitlines() if description else []

            # Initialize fields with default None to handle missing information
            enrolled = None
            course_number = None
            activity_number = None
            staff_members = None
            prospectus_link = None

            # Extract information based on specific keywords
            for line in description_lines:
                if line.startswith("Enrolled for this activity:"):
                    enrolled = line.split(":")[1].strip()
                elif line.startswith("Prospectus number course:"):
                    course_number = line.split(":")[1].strip()
                elif line.startswith("Prospectus number activity:"):
                    activity_number = line.split(":")[1].strip()
                elif line.startswith("Staff member(s):"):
                    staff_members = line.split(":")[1].strip()
                elif line.startswith("Prospectus:"):
                    prospectus_link = line.split(":")[1].strip()

            # Create the event dictionary with extracted values
            event = {
                'summary': component.get('summary'),
                'start': component.get('dtstart').dt,
                'end': component.get('dtend').dt,
                'description': description,  # Keep the full description for reference if needed
                'location': component.get('location'),
                'uid': component.get('uid'),
                'enrolled': enrolled,
                'course_number': course_number,
                'activity_number': activity_number,
                'staff_members': staff_members,
                'prospectus_link': prospectus_link,
            }
            timetable_events.append(event)

    # Print the extracted timetable events
    for event in timetable_events:
        print(f"Summary: {event['summary']}")
        print(f"Start: {event['start']}")
        print(f"End: {event['end']}")
        print(f"Description: {event['description']}")
        print(f"Location: {event['location']}")
        print(f"UID: {event['uid']}")
        print(f"Enrolled: {event['enrolled']}")
        print(f"Course Number: {event['course_number']}")
        print(f"Activity Number: {event['activity_number']}")
        print(f"Staff Members: {event['staff_members']}")
        print(f"Prospectus Link: {event['prospectus_link']}")
        print("-" * 40)
else:
    print("Failed to retrieve the timetable data. Status code:", response.status_code)