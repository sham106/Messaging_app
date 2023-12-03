# messaging/urls.py
from django.urls import path
from .views import send_message, agent_portal

urlpatterns = [
    path('send-message/', send_message, name='send_message'),
    path('agent-portal/', agent_portal, name='agent_portal'),
]
