from rest_framework import permissions
# import csv

class ModifyOwnProfile(permissions.BasePermission):
    """ this allows only intented user to modify there data"""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id