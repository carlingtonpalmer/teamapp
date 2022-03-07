from django.urls import include, path
from .import views

urlpatterns = [
    path('users/', views.AuthListView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
]