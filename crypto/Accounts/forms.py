from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(label="User Name",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your User Name'}))
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class RegisterForm(forms.Form):
    username=forms.CharField(label="User Name",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter  User Name'}))
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    confirmpassword=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email Address'}))
    