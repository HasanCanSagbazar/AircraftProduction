from rest_framework import permissions

class IsAssembleTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.team.is_assemble
