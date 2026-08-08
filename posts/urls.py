from django.urls import path

from .views import HelloWorldAPIView, PostAPIView, PostDetailAPIView

urlpatterns = [
    path('hello/', HelloWorldAPIView.as_view(), name='hello-world'),
    path('posts/', PostAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]
