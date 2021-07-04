from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.post_list_view),
    path('posts/<int:pk>/', views.post_detail_view),
    path('posts/<int:pk>/comments/', views.post_comment_view),
    path('post/', views.post_create_view),
    path('login/', views.login),
    path('register/', views.register),
]