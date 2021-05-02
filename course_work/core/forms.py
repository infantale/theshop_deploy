from django import forms

from .models import AdvUser

class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'last_name')
