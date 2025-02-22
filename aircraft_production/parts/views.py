from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Part
from .serializers import PartSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartFilter
from .permissions import IsTeamMember
from users.models import Role


class PartViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    
    #queryset = Part.objects.all_parts()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartFilter
    http_method_names = ['get', 'put', 'delete', 'post']


    def get_queryset(self):
        user = self.request.user
        if user.role == Role.COORDINATOR:
            return Part.objects.all()
        elif user.role in [Role.TEAM_LEAD, Role.EMPLOYEE]:
            return Part.objects.filter(team=user.team)
        return Part.objects.none()


    def get_permissions(self):
        if self.action == 'destroy':
            return [IsTeamMember()]
        return super().get_permissions()


    @action(detail=True, methods=['put'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        """Toggle the is_active status of a Part."""
        part = self.get_object()
        part.is_active = not part.is_active
        part.save()
        return Response({"is_active": part.is_active}, status=status.HTTP_200_OK)
