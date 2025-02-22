from rest_framework import viewsets, mixins, permissions
from .serializers import UAVSSerializer, UAVSStatusSerializer
from .models import Uavs
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsCoordinatorForPostPut


class UAVSViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    
    queryset = Uavs.objects.all_uavs()
    serializer_class = UAVSSerializer
    http_method_names = ['get', 'put', 'delete', 'post']
    permission_classes = [permissions.IsAuthenticated, IsCoordinatorForPostPut]
    

    @action(detail=True, methods=['put'], url_path='update-status')
    def update_status(self, request, pk=None):
        uav = self.get_object()
        serializer = UAVSStatusSerializer(uav, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

