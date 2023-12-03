from django.shortcuts import render
# messaging/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerMessage
from .forms import MessageForm, ReplyForm
from django.shortcuts import render, redirect



@api_view(['POST'])
def receive_message(request):
    # Implement logic to handle incoming messages and store in the database
    sender_name = request.data.get('sender_name')
    message_text = request.data.get('message_text')

    form = MessageForm({'sender_name': sender_name, 'message_text': message_text})
    if form.is_valid():
        form.save()
        return Response({'message': 'Message received and saved successfully'})
    else:
        return Response({'message': 'Invalid message data'}, status=400)
    return Response({'message': 'Message received successfully'})

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) 
            form.save()
            # Implement logic to send the message to the API endpoint
            return redirect('agent_portal')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})



def agent_portal(request):
    messages = CustomerMessage.objects.all()
    if request.method == 'POST':
        # Handle replies
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            message_id = request.POST.get('message_id')  # Assuming you have a hidden input in the form with the message ID
            customer_message = CustomerMessage.objects.get(pk=message_id)
            customer_message.agent_reply = reply_form.cleaned_data['agent_reply']
            customer_message.save()
            # Redirect or handle as needed

    else:
        reply_form = ReplyForm()

    return render(request, 'agent_portal.html', {'messages': messages, 'reply_form': reply_form})
    