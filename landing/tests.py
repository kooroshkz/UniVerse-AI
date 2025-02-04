# landing/tests.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
import datetime
from chatbot.models import CourseSchedule

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LandingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create timezone-aware datetimes
        now = timezone.now()
        CourseSchedule.objects.create(
            course_name="Course 1",
            course_type="Lecture",
            start_time=now + datetime.timedelta(days=1),
            end_time=now + datetime.timedelta(days=1, hours=2),
            locations="Building A",
            staffs="John Doe"
        )
        CourseSchedule.objects.create(
            course_name="Course 2",
            course_type="Seminar",
            start_time=now + datetime.timedelta(days=2),
            end_time=now + datetime.timedelta(days=2, hours=1),
            locations="Building B",
            staffs="Jane Doe"
        )

    def test_landing_view_shows_upcoming_events(self):
        # Replace 'landing_view' with your actual URL name if different
        url = reverse('landing_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        self.assertLessEqual(len(response.context['events']), 3)
        self.assertContains(response, "Upcoming Events")
