from django.urls import path
from . import views
from .views import profile

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profiles/', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('create-user/', views.create_user, name='create-user'),
    path('create-profile/', views.create_profile, name='create-profile')
]