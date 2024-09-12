from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
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

def Logout(request):
    return redirect('login')