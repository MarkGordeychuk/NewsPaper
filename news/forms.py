from django import forms
from django.contrib.auth.models import User

from .models import Post, Category


class PostForm(forms.ModelForm):
    # author = forms.ModelChoiceField(queryset=Author.objects, widget=forms.HiddenInput)

    class Meta:
        model = Post

        fields = [
            #'author',
            'category',
            'title',
            'content',
        ]


class SubscribeCategoryForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Подписки', required=False)
