from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='root'),
    path('projects/', views.ProjectListAPIView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),
    path('posts/', views.PostListAPIView.as_view(), name='posts'),
    path('services/', views.ServiceListAPIView.as_view(), name='services'),
]
