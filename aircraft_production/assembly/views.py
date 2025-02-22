# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from .models import UavsAssembly, AssemblyPart
from .serializers import UavsAssemblySerializer, AssemblyPartSerializer
from parts.models import Part
from .permissions import IsAssembleTeam


class UavsAssemblyViewSet(viewsets.GenericViewSet, 
                          viewsets.mixins.CreateModelMixin, 
                          viewsets.mixins.ListModelMixin, 
                          viewsets.mixins.RetrieveModelMixin):
    
    queryset = UavsAssembly.objects.all_assemblies()
    serializer_class = UavsAssemblySerializer
    permission_classes = [permissions.IsAuthenticated, IsAssembleTeam]

    def perform_create(self, serializer):
        user = self.request.user
        team = user.team
        added_by = user
        serializer.save(team=team, added_by=added_by)
    
    @action(detail=True, methods=['get'], url_path='get-parts')
    def get_parts(self, request, pk=None):
        """Get parts used in the specified assembly"""
        assembly = self.get_object()  
        parts = AssemblyPart.objects.filter(assembly=assembly)  
        parts_serializer = AssemblyPartSerializer(parts, many=True) 
        return Response(parts_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='add-parts')
    def add_parts(self, request, pk=None):
        assembly = self.get_object()

        if assembly.assembly_status == "Completed":
            return Response({"error": "Cannot add parts to a completed assembly"}, status=status.HTTP_400_BAD_REQUEST)

        part_ids = request.data.get('part_ids', [])

        if not part_ids:
            return Response({"error": "No part_ids provided"}, status=status.HTTP_400_BAD_REQUEST)

        parts = Part.objects.filter(id__in=part_ids)

        if parts.count() != len(part_ids):
            return Response({"error": "One or more parts not found"}, status=status.HTTP_404_NOT_FOUND)

        for part in parts:
            if AssemblyPart.objects.filter(assembly=assembly, part=part).exists():
                return Response({"error": f"Part {part.name} already added to this assembly"}, status=status.HTTP_400_BAD_REQUEST)

            if part.stock_quantity <= 0:
                return Response({"error": f"Part {part.name} is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

            if part.aircraft != assembly.aircraft_model:
                return Response({"error": f"Part {part.name} is not compatible with this {assembly.aircraft_model.name} aircraft model"}, status=status.HTTP_400_BAD_REQUEST)
        
            AssemblyPart.objects.create(assembly=assembly, part=part)

            part.stock_quantity -= 1
            part.save()

        assembly.check_and_update_status()

        return Response({"message": "Parts added successfully"}, status=status.HTTP_201_CREATED)


class AssemblyPartViewSet(viewsets.GenericViewSet, 
                          viewsets.mixins.CreateModelMixin, 
                          viewsets.mixins.ListModelMixin, 
                          viewsets.mixins.RetrieveModelMixin):
    
    queryset = AssemblyPart.objects.all_used_parts()
    serializer_class = AssemblyPartSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssembleTeam]


    @action(detail=True, methods=['post'], url_path='remove-part')
    def remove_part(self, request, pk=None):
        """Remove part from the assembly"""
        assembly = UavsAssembly.objects.get(pk=pk)
        part_id = request.data.get('part_id')
        part = Part.objects.get(id=part_id)

        assembly_part = AssemblyPart.objects.filter(assembly=assembly, part=part).first()
        if assembly_part:
            assembly_part.delete()
            return Response({"message": "Part removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Part not found in this assembly"}, status=status.HTTP_404_NOT_FOUND)
