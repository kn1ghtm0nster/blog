from django.urls import path
from .views import UserDetailApi, UserListApi, UserUpdateApi

urlpatterns = [
    path('users/', UserListApi.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailApi.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateApi.as_view(), name='user-update'),
]
