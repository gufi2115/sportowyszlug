from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ProfileM

class UserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForms(ModelForm):
    profile_image = forms.ImageField(
        label="Upload Profile Image",
        widget=forms.FileInput
    )
    class Meta:
        model = ProfileM
        fields = ['username', 'short_intro', 'profile_image']


    def __init__(self, *args, **kwargs):
        super(ProfileForms, self).__init__(*args, **kwargs)
