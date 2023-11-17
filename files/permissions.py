from rest_framework.permissions import BasePermission

class CanCreateFile(BasePermission):
    def has_permission(self,request,view):
        return request.user.has_permission('spaces.can_create_file')