from django.urls import path
from .views import dashboard, alerts

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('alerts/', alerts, name='alerts'),
]