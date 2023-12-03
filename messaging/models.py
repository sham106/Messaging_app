from django.db import models
from django.db import models

class CustomerMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    message_text = models.TextField()
    agent_reply = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_name} - {self.timestamp}'

