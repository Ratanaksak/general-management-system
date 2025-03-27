from django.contrib import admin
from .models import Department, Employee, Project

# Register models here
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to display in admin list

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'hire_date')  # Customize fields

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'status', 'start_date')  # Customize fields
    filter_horizontal = ('team_members',)  # For many-to-many field