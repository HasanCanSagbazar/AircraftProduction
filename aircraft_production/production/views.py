from rest_framework import mixins, viewsets, permissions
from .models import PartProduction
from .serializers import PartProductionSerializer
from .permissions import CanProduceOwnTeamParts

class PartProductionViewSet(
    mixins.CreateModelMixin,   
    mixins.ListModelMixin,     
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,   
    mixins.DestroyModelMixin,  
    viewsets.GenericViewSet    
):
    queryset = PartProduction.objects.all_part_productions()
    serializer_class = PartProductionSerializer
    http_method_names = ['get', 'put', 'delete', 'post']
    permission_classes = [permissions.IsAuthenticated, CanProduceOwnTeamParts]

    def get_permissions(self):
        """ Apply custom permission only for the 'create' action """
        if self.action == "create":
            return [CanProduceOwnTeamParts()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """ Automatically assign the currently authenticated user's team and set 'added_by' """
        user = self.request.user
        if user.team:  
            part_production = serializer.save(added_by=user, team=user.team)
            part = part_production.part
            part.stock_quantity += 1
            part.save()
        else:
            raise ValueError("User is not assigned to any team")
