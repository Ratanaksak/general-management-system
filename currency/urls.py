from django.urls import path
from .views import currency_converter

urlpatterns = [
    path('convert/', currency_converter, name='currency_converter'),
]