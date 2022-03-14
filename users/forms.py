from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, min_length=8, widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    level = forms.ChoiceField(choices=[("Level 1", "Level 1"),
                                       ("Level 2", "Level 2"),
                                       ("Level 3", "Level 3"),
                                       ("Level 4", "Level 4"),
                                       ("None of the above", "None of the above")])
    is_mentor = forms.BooleanField(help_text="Do you want to be a mentor?")

    class Meta:
        model = User
        fields = ('username', 'level', 'is_mentor', 'password1', 'password2')







