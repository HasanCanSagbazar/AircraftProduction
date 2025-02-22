from rest_framework import viewsets, mixins, permissions
from .serializers import TeamsSerializer
from .models import Team
from .permissions import TeamPermission


class TeamsViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    
    queryset = Team.objects.all_teams()
    serializer_class = TeamsSerializer
    http_method_names = ['get', 'put', 'delete', 'post']
    permission_classes = [permissions.IsAuthenticated, TeamPermission]

