from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Employee, Project
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm



@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace with your home URL name
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace with your home URL name
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def home_view(request):
    # Public view - no login required
    return render(request, 'index.html')

@login_required
def protected_view(request):
    # Requires login
    return render(request, 'dashboard.html')