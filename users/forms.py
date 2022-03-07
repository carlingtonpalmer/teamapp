from django.contrib.auth.admin import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password', '')


class CustomUserChangeForm(UserChangeForm):