# utils.py
from .models import Agent, CustomerMessage

def assign_messages_round_robin():
    agents = Agent.objects.all()
    messages = CustomerMessage.objects.filter(assigned_agent__isnull=True)

    for i, message in enumerate(messages):
        agent = agents[i % len(agents)]
        message.assigned_agent = agent
        message.save()