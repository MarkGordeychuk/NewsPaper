import django_filters
from django.forms import DateInput  # , CheckboxSelectMultiple

from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Название',
    )
    category = django_filters.ModelMultipleChoiceFilter(
        lookup_expr='exact',
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
        # widget=CheckboxSelectMultiple,
    )
    date_in = django_filters.DateFilter(
        lookup_expr='gt',
        label='Дата от',
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = []
