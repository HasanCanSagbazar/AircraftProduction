from django.db import models

class PartManager(models.Manager):
    """Custom manager for Team model."""

    def all_parts(self):
        """Return all part objects."""
        return self.all()
