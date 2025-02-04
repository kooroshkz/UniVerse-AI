from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import StaffMember, CourseSchedule

class ChatbotAPITest(TestCase):
    def setUp(self):
        # Create timezone-aware datetimes
        start_dt = timezone.make_aware(datetime.datetime(2025, 1, 1, 10, 0))
        end_dt = timezone.make_aware(datetime.datetime(2025, 1, 1, 12, 0))

        # Create test data
        self.staff = StaffMember.objects.create(name="Jane Doe", role="Lecturer")
        self.schedule = CourseSchedule.objects.create(
            course_name="Automata Theory",
            course_type="Lecture",
            start_time=start_dt,
            end_time=end_dt,
            locations="Building A",
            staffs="Jane Doe"
        )
        self.client = Client()

    def test_chatbot_staff_response(self):
        """Check database query for staff info."""
        url = reverse('chatbot_response')
        response = self.client.post(url, {'message': 'Who is Jane Doe?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())

    def test_chatbot_course_response(self):
        """Check database query for course schedule."""
        url = reverse('chatbot_response')
        response = self.client.post(url, {'message': 'When is Automata Theory?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())

    def test_chatbot_google_and_openai(self):
        """Check Google API + OpenAI usage (will fail if keys not set)."""
        url = reverse('chatbot_response')
        response = self.client.post(url, {'message': 'Search something on Google'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
