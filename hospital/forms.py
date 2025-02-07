from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [  'first_name','last_name','abha_id', 'email', 'password1', 'password2']
