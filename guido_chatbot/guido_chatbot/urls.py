from django.contrib import admin
from django.urls import path
from chatbot.views import chatbot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chatbot_view, name='chatbot')
]
