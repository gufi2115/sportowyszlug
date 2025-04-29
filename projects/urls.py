from django.urls import path
from . import views



urlpatterns = [
    path('projects/', views.projects, name="projects"),
    path('project/<int:pk>/', views.project, name="project"),
    path('create-project/', views.create_project, name="create-project"),
    path('update-project/<int:pk>/', views.updateproject, name="update-project"),
    path('delete-project/<int:pk>/', views.deleteproject, name="delete-project")
]