from django.urls import path
from . import views


urlpatterns = [
    path('request-quote/quoteType/', views.QuoteView.as_view()),
]