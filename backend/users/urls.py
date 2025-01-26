from django.urls import path
from .views import UserDetailApi, UserListApi, UserUpdateApi, UserDeleteApi

urlpatterns = [
    path('users/', UserListApi.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailApi.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateApi.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteApi.as_view(), name='user-delete'),
]
