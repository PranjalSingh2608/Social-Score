from django.urls import path
from .views import calculate_credit_score

urlpatterns = [
    path('', calculate_credit_score, name='calculate_credit_score'),
]
