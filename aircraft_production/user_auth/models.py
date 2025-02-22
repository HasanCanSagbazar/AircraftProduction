from django.db import models
from users.models import Employee
from .managers import OTPManager
from django.utils.timezone import now, timedelta
import uuid


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OTPManager()

    def __str__(self):
        return f"{self.employee.email} - {self.code}"
    
    def is_valid(self):
        """Checks if the OTP is still valid based on expiration time."""
        return now() < self.expires_at and not self.is_used
    
    def mark_used(self):
        """Marks the OTP as used."""
        self.is_used = True
        self.save()
    
    def save(self, *args, **kwargs):
        """Override save to set expiration time."""
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
