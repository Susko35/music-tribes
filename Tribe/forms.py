from django.forms import ModelForm
from .models import tribe

class CreateTribeForm(ModelForm):
    class Meta:
        model=tribe
        fields = ['name', 'genre', 'image']
