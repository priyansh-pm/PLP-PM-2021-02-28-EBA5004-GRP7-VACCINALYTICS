from django.urls import path
from .views import *

urlpatterns = [
    path('fact-checker', FactChecker.as_view()),
]