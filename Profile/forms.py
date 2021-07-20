from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import profile_info

class RegisterUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']
        
class EditAccountForm(ModelForm):
    class Meta:
        model = profile_info
        fields = ['profile_picture',]