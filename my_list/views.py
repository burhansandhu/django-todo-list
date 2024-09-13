from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from . import models
from django.utils  import timezone
from datetime import datetime
# Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('fn')
        last_name = request.POST.get('ln')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('signup')
        try:
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.save()
            messages.success(request, "Your account has been successfully created")
            return redirect('login')
        except:
            messages.error(request, "there is something issue try again")
            return redirect("signup")
        
    return render(request, 'signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
    return render(request,'login.html')

@login_required(login_url='/login/')
def Dashboard(request):
    return render(request, 'dashboard.html')


def create_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('create_task')

        today = timezone.now().date()

        if start_date_obj < today:
            messages.error(request, 'Start date cannot be in the past.')
            return redirect('create_task')

        if end_date_obj < start_date_obj:
            messages.error(request, 'End date must be equal to or greater than the start date.')
            return redirect('create_task')
        
        models.Task.objects.create(
            user=request.user,
            task_name=name,
            description=description,
            start_date=start_date_obj,
            end_date=end_date_obj,
            priority=priority,
            status = status
        )
        messages.success(request,"your task has been created successfully")
        return redirect('dashboard')

    return render(request, 'create_task.html')


def view_tasks(request):
    tasks = models.Task.objects.filter(user=request.user)
    return render(request, 'view_tasks.html', {'tasks': tasks})

def Logout(request):
    logout(request)
    return redirect('login')