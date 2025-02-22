from django.db import models

class TeamManager(models.Manager):
    """Custom manager for Team model."""

    def all_teams(self):
        """Return all team objects."""
        return self.all()
