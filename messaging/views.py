from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerMessage, Agent
from .forms import MessageForm, ReplyForm, ImportFileForm
from django.shortcuts import render, redirect
import csv, chardet
from django.db import transaction
import pandas as pd
from django.db import connection
from .utils import determine_urgency
from django.db.models import Q



@api_view(['POST'])
def receive_message(request):
    sender_name = request.data.get('sender_name')
    message_text = request.data.get('message_text')

    form = MessageForm({'sender_name': sender_name, 'message_text': message_text})
    if form.is_valid():
        is_urgent = determine_urgency(message_text)
        form.instance.is_urgent = is_urgent

        form.save()
        return Response({'message': 'Message received and saved successfully'})
    else:
        return Response({'message': 'Invalid message data'}, status=400)


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Save the message to get the message instance
            message = form.save()

            # Get the last assigned agent ID from the session
            last_assigned_agent_id = request.session.get('last_assigned_agent_id')

            # Get the agents excluding the last assigned agent
            agents = Agent.objects.exclude(id=last_assigned_agent_id)

            # If there are agents, assign the message to the next agent in line
            if agents.exists():
                next_agent = agents.first()
                message.assigned_agent = next_agent
                message.save()

                # Update the last assigned agent ID in the session
                request.session['last_assigned_agent_id'] = next_agent.id

                # Redirect to the agent_portal with the assigned agent_id
                return redirect('agent_portal', agent_id=next_agent.id)
            else:
                # No agents available for assignment
                return render(request, 'no_agents_available.html')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})



def agent_portal(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)

    query = request.GET.get('q')
    if query:
        # If a search query is provided, filter messages based on the query
        messages = CustomerMessage.objects.filter(
            Q(assigned_agent=agent) &
            (Q(message_text__icontains=query) | Q(sender_name__icontains=query))
        ).order_by('-is_urgent', '-timestamp')
    else:
        messages = CustomerMessage.objects.filter(assigned_agent=agent).order_by('-is_urgent', '-timestamp')
    reply_form = ReplyForm()

    if request.method == 'POST':
        print("Yeah you got me !!!")
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            message_id = request.POST.get('message_id')
            customer_message = get_object_or_404(CustomerMessage, pk=message_id, assigned_agent=agent)
            
            agent_reply_value = reply_form.cleaned_data['agent_reply']
            customer_message.agent_reply = agent_reply_value
            customer_message.save()

            print(f"Submitted agent_reply: {agent_reply_value}")
            print(f"Updated agent_reply: {customer_message.agent_reply}")

            return render(request, 'success_page.html')
        # Determine urgency for each message dynamically
    for message in messages:
        message.is_urgent = determine_urgency(message.message_text)

    return render(request, 'agent_portal.html', {'agent': agent, 'messages': messages, 'reply_form': reply_form})


def success_page(request):
    return render(request, 'success_page.html')


def upload_file(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the Excel file using pandas
            df = pd.read_excel(request.FILES['file'])
            df = df.rename(columns={'UserID': 'user_id', 'Timestamp (UTC)': 'timestamp', 'MessageBody': 'message_text'})
            CustomerMessage.objects.bulk_create(
                CustomerMessage(**row) for row in df.to_dict('records')
            )

            return redirect('agent_portal')  
    else:
        form = ImportFileForm()
    return render(request, 'upload.html', {'form': form})

def get_agent_ids():
    agents = Agent.objects.all()

    if agents.exists():
        agent_ids = [agent.pk for agent in agents]
        print(f"The IDs of all agents are: {agent_ids}")
    else:
        print("No agents found in the database.")

def assign_messages_round_robin(request):
    agents = Agent.objects.all()
    messages = CustomerMessage.objects.filter(assigned_agent__isnull=True)

    for i, message in enumerate(messages):
        agent = agents[i % len(agents)]
        message.assigned_agent = agent
        urgency_keywords = ['loan', 'disbursent']
        if any(keyword in message.message_text.lower() for keyword in urgency_keywords):
            message.is_urgent = True
        else:
            message.is_urgent = False
        message.save()
    get_agent_ids()
    return HttpResponse("Messages assigned successfully")

# def agent_portal(request, agent_id):
#     agent = Agent.objects.get(id=agent_id)
#     messages = CustomerMessage.objects.filter(assigned_agent=agent)
#     return render(request, 'agent_portal.html', {'agent': agent, 'messages': messages})  

def agent_reply(request, message_id):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')  # Get message_id from form data
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            customer_message = get_object_or_404(CustomerMessage, pk=message_id)
            customer_message.agent_reply = reply_form.cleaned_data['agent_reply']
            customer_message.save()
            return redirect('agent_portal', customer_message.assigned_agent.id)
    return redirect('agent_portal', message_id)  # Redirect to agent portal with message_id
