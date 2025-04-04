from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Employee, Project
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, HttpResponse
from .forms import FileUploadForm
from .utils.converter import convert_pdf_to_word, convert_image_to_word
from django.conf import settings
import os
from datetime import datetime
import logging
from django.http import JsonResponse



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


logger = logging.getLogger(__name__)

def file_converter(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = request.FILES['file']
                file_name = uploaded_file.name.lower()
                
                # Validate file type
                if not (file_name.endswith('.pdf') or 
                       file_name.endswith(('.jpg', '.jpeg', '.png'))):
                    return JsonResponse({'error': 'Unsupported file format'}, status=400)
                
                # Create temp directory if not exists
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_files')
                os.makedirs(temp_dir, exist_ok=True)
                
                # Save uploaded file
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Conversion logic
                if file_name.endswith('.pdf'):
                    doc = convert_pdf_to_word(temp_path)
                else:  # Image
                    doc = convert_image_to_word(temp_path)
                
                # Create response
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename=converted_{os.path.splitext(uploaded_file.name)[0]}.docx'
                doc.save(response)
                
                # Clean up
                os.remove(temp_path)
                
                return response
                
            except Exception as e:
                logger.error(f"Conversion error: {str(e)}", exc_info=True)
                return JsonResponse({'error': str(e)}, status=500)
            
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    
    form = FileUploadForm()
    return render(request, 'converter/convert.html', {'form': form})