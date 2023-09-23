from django import forms
from .models import Post, Subscribers


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['header', 'text', 'author', 'category']


class SubscribeForm(forms.Form):
    pass

