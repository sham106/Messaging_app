from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomerMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    message_text = models.TextField()
    agent_reply = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assigned_agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    user_id = models.CharField(max_length=100,  null=True)
    is_urgent = models.BooleanField(default=False)



    def __str__(self):
        return f'{self.sender_name} - {self.timestamp}'

