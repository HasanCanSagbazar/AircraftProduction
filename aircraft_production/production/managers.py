from django.db import models

class PartProductionManager(models.Manager):
    """Custom manager for Team model."""

    def all_part_productions(self):
        """Return all part objects."""
        return self.all()
