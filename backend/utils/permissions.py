from rest_framework.permissions import BasePermission

class IsProductManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Product Managers').exists()