from django.urls import path
from .views import calculate_credit_score,calculate_hr

urlpatterns = [
    path('', calculate_credit_score, name='calculate_credit_score'),
    path('hr/', calculate_hr, name='calculate_hr'),
]
