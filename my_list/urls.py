
from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/',views.Login, name='login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('logout/', views.Logout, name='logout'),
]
