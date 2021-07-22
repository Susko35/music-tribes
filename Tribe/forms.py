from django.forms import ModelForm
from .models import tribe, message

class CreateTribeForm(ModelForm):
    class Meta:
        model=tribe
        fields = ['name', 'genre', 'image']

class CreateMessageForm(ModelForm):
    class Meta:
        model = message
        fields=['text',]