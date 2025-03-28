from rest_framework import permissions

class CheckDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'doctor':
            return True
        return False


class CheckPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'patient':
            return True
        return False