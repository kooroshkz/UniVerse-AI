from django.contrib import admin
from django.urls import path, include
from chatbot.views import chatbot_view, chatbot_response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chatbot_view, name='chatbot'),
    path('chatbot_response/', chatbot_response, name='chatbot_response'),
    path('calendar/', include('lucalendar.urls'))
]