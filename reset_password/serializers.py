from rest_framework import serializers
from django.conf import settings

# reset password
from rest_auth import serializers as rest_serializer
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class ResetPasswordSerializer(rest_serializer.PasswordResetSerializer):
    pass

# class ChangePasswordSerializer(rest_serializer.PasswordChangeSerializer):
    # pass

# class TestConfirmSerializer(rest_serializer.PasswordResetConfirmSerializer):

#    pass