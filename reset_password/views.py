from rest_framework import generics
from django.contrib.auth import views as auth_views
# reset password
from rest_auth import views as rest_view
from . import serializers

# Create your views here.

class RestPasswordView(rest_view.PasswordResetView):
    pass

class ChangePasswordView(rest_view.PasswordChangeView):
    pass

# class ResetPasswordConfirmView(rest_view.PasswordResetConfirmView):
#     pass

class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    pass

class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    pass

