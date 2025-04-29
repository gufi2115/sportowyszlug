from django.contrib.admin.templatetags.admin_list import search_form
from django.forms import ModelForm
from django import forms
from .models import ProjectM, ReviewM

class ProjectForm(ModelForm):
    class Meta:
        model = ProjectM
        fields = ['title', 'video', 'age', 'time']

    title = forms.CharField(
        label="Project Title",
        widget= forms.TextInput(attrs={
            'placeholder': 'Project Title'
        })
    )

    video = forms.CharField(
        label="Project Title",
        widget= forms.TextInput(attrs={
            'placeholder': 'Your Video'
        })
    )

    age = forms.IntegerField(label="Your age",
                             widget= forms.NumberInput(attrs={
                                 'placeholder': 'Your Age',
                             }))

    time = forms.IntegerField(label="Your time",
                             widget=forms.NumberInput(attrs={
                                 'placeholder': 'Your Time',
                             }))


class ReviewForm(ModelForm):
    class Meta:
        model = ReviewM
        fields = [ 'body' ,'value']
