from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

# from news.models import Category


class UserForm(forms.ModelForm):
    # categories_subscribed = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            # 'categories_subscribed',
        ]


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
