from rest_framework import viewsets, mixins, permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    """API for managing Employees"""
    permission_classes = [permissions.IsAuthenticated]

    queryset = Employee.objects.all_employees()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'put']

