from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import UserForm
from news.forms import SubscribeCategoryForm


class UserDetail(DetailView):
    model = User
    template_name = 'user.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = hasattr(self.object, 'author')
        context['is_current_user'] = self.request.user == self.get_object()
        context['subscribe_form'] = SubscribeCategoryForm(
            initial={'categories': [cat['pk'] for cat in self.object.categories_subscribed.values('pk')]}
        )
        return context


class UserUpdate(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_edit.html'
    permission_required = ('auth.change_user', )

    def has_permission(self):
        return True if self.request.user == self.get_object() else super().has_permission()

    def get_success_url(self):
        return reverse('accounts', kwargs={'pk': self.object.pk})
