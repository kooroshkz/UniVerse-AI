from django.urls import path
from .views import chatbot_view, chatbot_response, validate_tokens, add_timetable


urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('response/', chatbot_response, name='chatbot_response'),
    path('validate_tokens/', validate_tokens, name='validate_tokens'),
    path('add-timetable/', add_timetable, name='add_timetable'),
]
