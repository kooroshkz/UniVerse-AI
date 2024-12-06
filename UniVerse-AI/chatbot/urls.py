from django.urls import path
from .views import chatbot_view, chatbot_response

urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('response/', chatbot_response, name='chatbot_response'),
]
