from django.urls import path
from .views import (
    BlogpostListApi,
    BlogpostCreateApi
)

urlpatterns = [
    path('posts/', BlogpostListApi.as_view(), name='post-list'),
    path('posts/create/', BlogpostCreateApi.as_view(), name='post-create'),
]
