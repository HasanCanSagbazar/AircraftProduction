from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Role

class TeamPermission(BasePermission):
    """
    - Coordinator can perform all methods (GET, POST, PUT, DELETE).
    - Team Lead can only perform GET and PUT.
    - Employee can only perform GET.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.role == Role.COORDINATOR:
                return True
            elif request.user.role == Role.TEAM_LEAD and request.method in ["PUT", "GET"]:
                return True
            elif request.user.role == Role.EMPLOYEE and request.method == "GET":
                return True
        
        return False
