from django import forms

from .models import CustomerMessage

class MessageForm(forms.ModelForm):
   class Meta:
        model = CustomerMessage
        fields = ['sender_name', 'message_text']