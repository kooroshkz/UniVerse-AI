from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('calendar/', include('lucalendar.urls')),
]
