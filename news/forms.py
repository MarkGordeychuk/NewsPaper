from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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

        labels = {
            'category': _('Category'),
            'title': _('Title'),
            'content': _('Content'),
        }


class SubscribeCategoryForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label=_('Subscribes'), required=False)
