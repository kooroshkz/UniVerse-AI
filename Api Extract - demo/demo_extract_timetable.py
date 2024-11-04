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
            event = {
                'summary': component.get('summary'),
                'start': component.get('dtstart').dt,
                'end': component.get('dtend').dt,
                'description': component.get('description'),
                'location': component.get('location'),
                'uid': component.get('uid'),
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
        print("-" * 40)
else:
    print("Failed to retrieve the timetable data. Status code:", response.status_code)
