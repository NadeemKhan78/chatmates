from django import forms
from django.forms import ModelForm
from .models import ChatMessage, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "message-input", "cols": "5", "rows": "1", "placeholder": "Type message here"}))

    class Meta:
        model = ChatMessage
        fields = ["body",]


class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter lastname'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm password'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class ProfileForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter lastname'}))
    pic = forms.ImageField(widget=forms.FileInput)
    
    class Meta:
        model = Profile
        fields = ['name', 'first_name', 'last_name', 'pic']
