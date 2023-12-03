# messaging/urls.py
from django import views
from django.urls import path
from .views import send_message, agent_portal, upload_file, success_page

urlpatterns = [
    path('send-message/', send_message, name='send_message'),
    path('agent-portal/', agent_portal, name='agent_portal'),
    path('import-csv/', upload_file, name='import_csv'),
    path('success-page/', success_page, name='success_page'),

]
