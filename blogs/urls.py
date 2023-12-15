from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.user_logout, name='user_logout'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),

]
