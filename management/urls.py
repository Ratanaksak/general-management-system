from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, login_view
from django.contrib.auth.decorators import login_required
from .views import home_view, protected_view
urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', login_required(protected_view), name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('employees/', views.employee_list, name='employee_list'),
    path('projects/', views.project_list, name='project_list'),
    path('departments/', views.department_list, name='department_list'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]