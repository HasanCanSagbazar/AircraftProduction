import uuid
import random
import string
from django.db import models
from parts.models import Part
from teams.models import Team
from users.models import Employee
from .managers import PartProductionManager

class PartProduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=50, 
        choices=[('Produced', 'Produced'), ('Recycled', 'Recycled')], 
        default='Produced'
    )
    serial_number = models.CharField(max_length=100, unique=False, default="000000", blank=True)
    is_used = models.BooleanField(default=False)
    added_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PartProductionManager()

    def __str__(self):
        return f"{self.part.name} - {self.status}"

    def generate_serial_number(self):
        return ''.join(random.choices(string.digits, k=6))  
    
    def save(self, *args, **kwargs):
        if self.serial_number == "000000" or not self.serial_number:  
            self.serial_number = self.generate_serial_number()
            while PartProduction.objects.filter(serial_number=self.serial_number).exists():  
                self.serial_number = self.generate_serial_number()  
        super().save(*args, **kwargs)
