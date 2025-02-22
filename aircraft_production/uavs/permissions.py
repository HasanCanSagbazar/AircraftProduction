from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Role

class IsCoordinatorForPostPut(BasePermission):
    """
    - Everyone can access GET (list) operations.
    - Only Coordinator can perform POST and PUT operations.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and request.user.role == Role.COORDINATOR
