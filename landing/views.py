from django.shortcuts import render
from django.utils import timezone
from chatbot.models import CourseSchedule

def merge_events(events):
    """
    Merges events based on course name and type, combining their time ranges and locations.
    """
    merged = {}
    for event in events:
        key = (event.course_name, event.course_type)
        if key not in merged:
            merged[key] = {
                'course_name': event.course_name,
                'course_type': event.course_type,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'locations': set(event.locations.split(', '))  # Use a set to avoid duplicates
            }
        else:
            # Update the end time if the new event ends later
            merged[key]['end_time'] = max(merged[key]['end_time'], event.end_time)
            # Add the new location(s)
            merged[key]['locations'].update(event.locations.split(', '))

    # Convert the locations back to a comma-separated string
    for key in merged:
        merged[key]['locations'] = ', '.join(merged[key]['locations'])

    # Return a list of merged events
    return list(merged.values())

def landing_view(request):
    # Fetch the three closest upcoming events using timezone-aware datetime
    upcoming_events = CourseSchedule.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    merged_events = merge_events(upcoming_events)[:3]  # Limit to the top 3 merged events
    return render(request, 'landing/index.html', {'events': merged_events})