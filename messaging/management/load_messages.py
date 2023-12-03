# messaging/management/commands/load_messages.py

import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from messaging.models import CustomerServiceMessage

class Command(BaseCommand):
    help = 'Load customer service messages from CSV'

    def handle(self, *args, **options):
        csv_file_path = 'GeneralistRails_Project_MessageData_1.csv'  # Update with the actual path
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert timestamp string to datetime
                row['timestamp'] = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                CustomerServiceMessage.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Successfully loaded messages from CSV.'))
