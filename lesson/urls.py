from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('assessment/', views.assessment, name='assessment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/register', views.register, name='register'),
    path('study-plan/<int:plan_id>/', views.study_plan_detail, name='study_plan_detail'),
    path('update-session/<int:session_id>/', views.update_session_status, name='update_session_status'),
]