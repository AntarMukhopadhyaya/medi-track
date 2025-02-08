from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Feedback

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [  'first_name','last_name','abha_id', 'email', 'password1', 'password2']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['recipient', 'rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }