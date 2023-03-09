from django import forms
from .models import Post, Author
from django.contrib.auth.models import User, Group





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['header', 'text', 'author', 'category']



