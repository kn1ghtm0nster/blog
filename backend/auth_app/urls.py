from django.urls import path
from .views import RegisterUserApi, ObtainTokenApi

urlpatterns = [
    path('register/', RegisterUserApi.as_view(), name='register'),
    path('token/', ObtainTokenApi.as_view(), name='token_obtain'),
]
