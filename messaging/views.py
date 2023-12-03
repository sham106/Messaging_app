from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerMessage
from .forms import MessageForm, ReplyForm, ImportFileForm
from django.shortcuts import render, redirect
import csv, chardet
from django.db import transaction
import pandas as pd
from django.db import connection


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


def success_page(request):
    return render(request, 'success_page.html')


def upload_file(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the Excel file using pandas
            df = pd.read_excel(request.FILES['file'])
            df = df.rename(columns={'UserID': 'user_id', 'Timestamp (UTC)': 'timestamp', 'MessageBody': 'message_text'})

            # Save the data to the database
            # CustomerMessage.objects.all().delete()  # Optional: Clear existing data
            CustomerMessage.objects.bulk_create(
                CustomerMessage(**row) for row in df.to_dict('records')
            )

            return redirect('agent_portal')  # Redirect to a success page
    else:
        form = ImportFileForm()
    return render(request, 'upload.html', {'form': form})
# def detect_encoding(content):
#     detector = chardet.UniversalDetector()
#     detector.feed(content)
#     detector.close()
#     detected_encoding = detector.result['encoding']
#     return detected_encoding if detected_encoding else 'utf-8'

# def import_csv(request):
#     if request.method == 'POST':
#         form = CSVImportForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Get the uploaded CSV file
#             uploaded_file = request.FILES['csv_file']

#             # Read the CSV file content
#             uploaded_content = uploaded_file.read()

#             # Detect the encoding using chardet
#             csv_encoding = detect_encoding(uploaded_content)

#             try:
#                 # Try to decode the content using the detected encoding
#                 csv_content = uploaded_content.decode(csv_encoding)
#             except UnicodeDecodeError:
#                 # If decoding fails, use 'utf-8' as a fallback
#                 csv_content = uploaded_content.decode('utf-8', errors='replace')

#             # Split the content into lines
#             csv_lines = csv_content.splitlines()
#             print(csv_lines)

#             csv_reader = csv.DictReader(csv_lines)

#             with transaction.atomic():  # Ensure atomic transaction
#                 for row in csv_reader:
#                     if 'UserID' in row:
#                         # Check for the existence of the 'UserID' key
#                         CustomerMessage.objects.create(
#                             user_id=row['UserID'],
#                             timestamp=row['Timestamp'],
#                             message_text=row['MessageBody'],
#                         )

#             return redirect('success_page')  # Redirect to a success page
#     else:
#         form = CSVImportForm()

#     return render(request, 'import.html', {'form': form})

# def import_data(file_path):
#     data = pd.read_excel(file_path)
#     for index, row in data.iterrows():
#         my_model = CustomerMessage()
#         my_model.message_text = row['field1']
#         my_model.timestamp = row['field2']
#         my_model.user_id = row['field3']
#         my_model.save()

# def import_data(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         if file.name.endswith('.xlsx'):
#             df = pd.read_excel(file)
#             # Do something with the data
#             engine = connection.cursor()
#             df.to_sql('table_name', engine, if_exists='replace', index=False)
#             return render(request, 'success.html')
#         else:
#             return HttpResponseBadRequest('Invalid file type. Please upload a file with a .xlsx extension.')
#     else:
#         return render(request, 'upload.html')