from django.db import models
from .managers import TeamManager
import uuid


class Team(models.Model):
    TEAM_CHOICES = [
        ('wing', 'Kanat Takımı'),
        ('body', 'Gövde Takımı'),
        ('tail', 'Kuyruk Takımı'),
        ('avionics', 'Aviyonik Takımı'),
        ('assembly', 'Montaj Takımı'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=TEAM_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    is_assemble = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TeamManager()

    def save(self, *args, **kwargs):
        """Automatically set is_assemble and is_producer based on the team type."""
        if self.name == 'assembly':
            self.is_assemble = True
            self.is_producer = False
        else:
            self.is_assemble = False
            self.is_producer = True
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
