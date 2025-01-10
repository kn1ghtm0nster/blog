from django.urls import path
from .views import RegisterUserApi

urlpatterns = [
    path('register/', RegisterUserApi.as_view(), name='register'),
]
