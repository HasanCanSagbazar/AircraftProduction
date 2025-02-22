from django.db import models
from .managers import UAVSManager
import uuid

class Uavs(models.Model):
    STATUS = {  
        ("In Prod", "Üretimde"),
        ("Out Prod", "Üretimde Değil"),
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=STATUS, default='In Prod')
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UAVSManager()

    def __str__(self):
        return f"{self.name} ({self.model})"