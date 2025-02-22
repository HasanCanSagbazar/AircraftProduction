from rest_framework import permissions
from parts.models import Part


class CanProduceOwnTeamParts(permissions.BasePermission):
    """
    Users can only produce parts assigned to their own team.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to create a production for the part's team.
        """
        if view.action == 'create':
            part_id = request.data.get('part')  
            part = Part.objects.get(id=part_id)
            if part.team and request.user.team != part.team:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if not obj.part.team:
            return False

        return request.user.team == obj.part.team
