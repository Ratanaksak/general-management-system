from django.db import models
from django.contrib.auth.models import User
from .models import Department, Employee, Project  # Path to your models
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(Employee, related_name='projects')
    status = models.CharField(max_length=20, choices=[
        ('PLANNING', 'Planning'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ])
    
    def __str__(self):
        return self.name