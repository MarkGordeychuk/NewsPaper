from django.urls import path

from .views import ptype_views, IndexView, become_author, subscribe_category


urlpatterns = [
    *[path(url, cls.as_view(), **kwargs) for url, cls, kwargs in ptype_views.get_urlpattern()],
    path('', IndexView.as_view()),
    path('accounts/becomeauthor/', become_author, name='account_become_author'),
    path('accounts/subscribe/', subscribe_category, name='news_subscribe_category'),
]
