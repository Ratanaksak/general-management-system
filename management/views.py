from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Employee, Project
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from .forms import VideoDownloadForm
import os
import yt_dlp
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



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


# views.py


@csrf_exempt  # Only if you don't want to deal with CSRF token issues for now
def download_video(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')
        format_choice = request.POST.get('format')

        if not video_url:
            return HttpResponse("No video URL provided.", status=400)

        try:
            output_dir = "downloads"
            os.makedirs(output_dir, exist_ok=True)

            # Set output template
            output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
            }

            if format_choice == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:  # mp4
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

            # After download, find correct file
            if format_choice == 'mp3':
                filename = filename.rsplit('.', 1)[0] + ".mp3"

            # Serve file as response
            response = FileResponse(open(filename, 'rb'), as_attachment=True)

            # Optional: Clean up after download
            # os.remove(filename)

            return response

        except Exception as e:
            print("Error:", e)
            return HttpResponse("An error occurred during download.", status=500)

    return render(request, 'download.html')
