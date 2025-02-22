from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Role

class IsTeamMember(BasePermission):
    """
    Custom permission to allow users to delete only their team's parts.
    """

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            user_team = request.user.team
            part_team = obj.team

            return user_team == part_team
        return True
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.role == Role.COORDINATOR:
                return True
            elif request.user.role == Role.TEAM_LEAD and request.method in ["POST", "PUT", "GET"]:
                return True
            elif request.user.role == Role.EMPLOYEE and request.method == "GET":
                return True
        
        return False

