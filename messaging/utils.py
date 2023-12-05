# utils.py
from .models import Agent, CustomerMessage
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def assign_messages_round_robin():
    agents = Agent.objects.all()
    messages = CustomerMessage.objects.filter(assigned_agent__isnull=True)

    for i, message in enumerate(messages):
        agent = agents[i % len(agents)]
        message.assigned_agent = agent
        message.save()



nltk.download('punkt')
nltk.download('stopwords')

def determine_urgency(message_text):
    keywords = ['loan', 'approval', 'disbursed'] 
    tokens = word_tokenize(message_text.lower())
    
    return any(keyword in tokens for keyword in keywords)
