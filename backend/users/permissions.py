# permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        print("!!!!!!!!!!! "+request.user.role)
        return request.user and request.user.role == 'admin'

class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'worker']

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'member'