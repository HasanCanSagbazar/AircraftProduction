from django.db import models
from uavs.models import Uavs
from .managers import PartManager
from teams.models import Team
import uuid


class Part(models.Model):
    PART_CATEGORIES = [
        ('tail', 'Kuyruk'),
        ('body', 'Gövde'),
        ('avionic', 'Aviyonik'),
        ('wing', 'Kanat'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aircraft = models.ForeignKey(Uavs, on_delete=models.CASCADE, related_name="parts")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=PART_CATEGORIES)
    description = models.TextField(blank=True, null=True) 
    serial_number = models.CharField(max_length=100, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PartManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'aircraft'], name='unique_part_per_aircraft')
        ]

    def __str__(self):
        return self.name
