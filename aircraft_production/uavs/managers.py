from django.db import models

class UAVSManager(models.Manager):
    """Custom manager for Team model."""

    def all_uavs(self):
        """Return all uav objects."""
        return self.all()
