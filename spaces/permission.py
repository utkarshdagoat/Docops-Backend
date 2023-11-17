from django.db.models.fields import return_None
from requests import request
from rest_framework.permissions import BasePermission , SAFE_METHODS

from .services import IsUserInSpace


class IsInSpace(BasePermission):
    '''
    Custom permissions to check if the owner can create a file
    '''
    def has_object_permission(self , request,view , obj):
        is_user_in_space = IsUserInSpace(obj=obj , user=request.user)
        return is_user_in_space

class IsTheCreater(BasePermission):
    def is_the_creater(self,request , view , obj):
        return request.user == obj.creater


