# messaging/urls.py
from django import views
from django.urls import path
from .views import send_message, agent_portal, upload_file, success_page, assign_messages_round_robin, agent_reply

print("URL pattern matched!")
urlpatterns = [
    path('send-message/', send_message, name='send_message'),
    # path('general-agent-portal/', agent_portal, name='general_agent_portal'),
    path('import-csv/', upload_file, name='import_csv'),
    path('success-page/', success_page, name='success_page'),
    path('assign-messages/', assign_messages_round_robin, name='assign_messages_round_robin'),
    path('agent-portal/<int:agent_id>/', agent_portal, name='agent_portal'),
    path('agent-reply/<int:message_id>/', agent_reply, name='agent_reply'),


]
