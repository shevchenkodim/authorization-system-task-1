from django import forms
from django.forms import ModelForm
from .models import User


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=100, required=True)


class UserRegisterForm(ModelForm):
    otp_code = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class CollaboratorRegisterForm(ModelForm):
    otp_code = forms.IntegerField(required=True)
    password2 = forms.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']


class CollaboratorLoginForm(forms.Form):
    otp_code = forms.IntegerField(required=True)
    phone_number = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=128, required=True)


class UserLoginForm(forms.Form):
    otp_code = forms.IntegerField(required=True)
    phone_number = forms.CharField(max_length=100, required=True)
