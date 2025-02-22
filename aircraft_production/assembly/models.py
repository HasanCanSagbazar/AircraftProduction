from django.db import models
from teams.models import Team
from parts.models import Part
from uavs.models import Uavs
from users.models import Employee
from .managers import UavsAssemblyManager, AssemblyPartManager
import uuid


class UavsAssembly(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aircraft_model = models.ForeignKey(Uavs, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    assembly_status = models.CharField(
        max_length=50,
        choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='In Progress'
    )
    added_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UavsAssemblyManager()

    def __str__(self):
        return f"{self.aircraft_model.name} Assembly - {self.assembly_status}"
    

    def check_and_update_status(self):
        required_parts = self.aircraft_model.parts.all()

        all_parts_added = all(
            AssemblyPart.objects.filter(assembly=self, part=part).exists() for part in required_parts
        )

        if all_parts_added:
            self.assembly_status = "Completed"
            self.save()

            self.aircraft_model.stock_quantity += 1
            self.aircraft_model.save()


class AssemblyPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assembly = models.ForeignKey(UavsAssembly, on_delete=models.CASCADE, related_name="assembly_parts")  
    part = models.ForeignKey(Part, on_delete=models.CASCADE) 
    installed_at = models.DateTimeField(auto_now_add=True)

    objects = AssemblyPartManager()

    def __str__(self):
        return f"{self.part.name} for {self.assembly.aircraft_model.name}"
