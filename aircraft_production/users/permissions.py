from rest_framework.permissions import BasePermission
from .models import Role

class IsCoordinator(BasePermission):
    """Only users with Coordinator role can access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.COORDINATOR

class IsTeamLead(BasePermission):
    """Only users with Team Lead role can access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.TEAM_LEAD

class IsEmployee(BasePermission):
    """Only users with Employee role can access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.EMPLOYEE
