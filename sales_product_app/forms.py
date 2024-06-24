from django import forms
from django.db import models
from django.forms import ModelForm
from imagekit.forms import ProcessedImageField
from pilkit.processors import ResizeToFill

from .models import CustomUser


class UserForm(ModelForm):
    username = forms.TextInput()
    thumbnail = forms.ImageField()
    class Meta:
        model = CustomUser
        fields = ['username', 'thumbnail']