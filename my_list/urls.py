
from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/',views.Login, name='login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('create-task/',views.create_task, name='create_task'),
    path('view-tasks/',views.view_tasks,name='view_tasks'),
    path('logout/', views.Logout, name='logout'),
]
