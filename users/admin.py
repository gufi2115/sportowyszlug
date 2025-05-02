from django.contrib import admin
from .models import ProfileM
from django.db import models
from django import forms

admin.site.register(ProfileM)

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'Widget': forms.FileInput}
    }