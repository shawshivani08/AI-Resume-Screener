from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_resume, name='upload'),
    
    path("job-description/", views.job_description, name="job_description"),
    path("ranking/", views.ranking, name="ranking"),
]