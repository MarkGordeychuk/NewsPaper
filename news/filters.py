import django_filters
from django.forms import DateInput  # , CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label=_('Title'),
    )
    category = django_filters.ModelMultipleChoiceFilter(
        lookup_expr='exact',
        queryset=Category.objects.all(),
        label=_('Category'),
        conjoined=True,
        # widget=CheckboxSelectMultiple,
    )
    date_in = django_filters.DateFilter(
        lookup_expr='gt',
        label=_('Date in'),
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = []
