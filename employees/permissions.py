from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission

class IsAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser and obj.branch.organization == request.user.branch.organization

class IsBranchAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_delegate and obj.branch == request.user.branch


class IsOrgAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser and obj.admin_user == request.user.adminuser
    
class IsSafeOrPutOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'PUT':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'PUT':
            return True
        return False

class IsMasterAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_master_admin