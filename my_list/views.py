from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from . import models
from django.utils  import timezone
from datetime import datetime
from django.db.models import Case, When, Value, IntegerField
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
    sort_option = request.GET.get('sort_by', 'start_date')

    # Define sorting options
    sort_options_map = {
        'start_date': 'start_date',
        'end_date': 'end_date',
        'priority': 'custom_priority',  # Custom sorting for priority
        'status': 'status',
    }

    # Get user's tasks
    tasks = models.Task.objects.filter(user=request.user)

    # Custom sorting for priority
    if sort_option == 'priority':
        tasks = tasks.annotate(
            custom_priority=Case(
                When(priority='High', then=Value(1)),  # 'High' from model
                When(priority='Medium', then=Value(2)),  # 'Medium' from model
                When(priority='Low', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('custom_priority')
    elif sort_option in sort_options_map:
        tasks = tasks.order_by(sort_options_map[sort_option])

    return render(request, 'dashboard.html', {'tasks': tasks, 'sort_option': sort_option})



@login_required(login_url='/login/')
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




@login_required(login_url='/login/')
def update_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task_name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        # Convert string dates to datetime objects for comparison
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('update_task', task_id=task_id)


        if end_date_obj < start_date_obj:
            messages.error(request, 'End date must be equal to or greater than the start date.')
            return redirect('update_task', task_id=task_id)

        # Update the task with the new data
        task.task_name = task_name
        task.description = description
        task.start_date = start_date_obj
        task.end_date = end_date_obj
        task.priority = priority
        task.status = status
        task.save()

        messages.success(request, 'Task updated successfully.')
        return redirect('dashboard')

    return render(request, 'update_task.html', {'task': task})
    

@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect('login')