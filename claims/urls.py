from django.urls import path
from . import views

urlpatterns = [
    path('claims/', views.ClaimsView.as_view()),
]