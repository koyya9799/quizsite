from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/add-quiz/', views.add_quiz_view, name='add_quiz'),
    path('admin-dashboard/delete-quiz/<int:quiz_id>/', views.delete_quiz_view, name='delete_quiz'),
    path('admin-dashboard/add-question/<int:quiz_id>/', views.add_question_view, name='add_question'),
    path('admin-dashboard/questions/<int:quiz_id>/', views.show_questions_view, name='show_questions'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz_view, name='start_quiz'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),





]
