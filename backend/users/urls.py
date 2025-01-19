from django.urls import path
from .views import UserDetailApi, UserListApi

urlpatterns = [
    path('users/', UserListApi.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailApi.as_view(), name='user-detail'),
]
