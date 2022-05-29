from django.urls import path, reverse_lazy

from .views import UserDetail, UserUpdate


urlpatterns = [
    path('<int:pk>', UserDetail.as_view(), name='accounts'),
    path('<int:pk>/update/', UserUpdate.as_view(), name='accounts_update'),
]

