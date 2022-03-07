from django.urls import path, include
from . import views 


urlpatterns = [
    path('claim-forms/', views.ClaimFormView.as_view()),
]