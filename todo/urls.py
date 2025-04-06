from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),  
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('todos/', views.todos, name='todos'), 
    path('todos/<int:todo_id>/done/', views.mark_done, name='mark_done'),
    path('todos/<int:todo_id>/edit/', views.edit_task, name='edit_task'),
    path('todos/<int:todo_id>/update_date/', views.update_task_date, name='update_task_date'),
    path('todos/delete_finished/', views.delete_finished_tasks, name='delete_finished_tasks'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),  
]