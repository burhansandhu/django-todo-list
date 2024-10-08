
from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/',views.Login, name='login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('create-task/',views.create_task, name='create_task'),
    path('update-task/<int:task_id>/',views.update_task,name='update_task'),
    path('logout/', views.Logout, name='logout'),
]
