from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == 'GET' or admin_permission


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj ):
        admin_permission = bool(request.user and request.user.is_staff)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user or admin_permission
