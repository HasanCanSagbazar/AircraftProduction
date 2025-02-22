from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import EmployeeManager
from teams.models import Team
import uuid

class Role(models.TextChoices):
    COORDINATOR = "COORDINATOR", "Coordinator"
    TEAM_LEAD = "TEAM_LEAD", "Team Lead"
    EMPLOYEE = "EMPLOYEE", "Employee"



class Employee(AbstractUser):
    SHIFT_CHOICES = [
        ("MORNING", "08:00 - 16:00"),
        ("EVENING", "16:00 - 00:00"),
        ("NIGHT", "00:00 - 08:00"),
    ]

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True)
    phone_number_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="employees"
    )
    position = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    shift = models.CharField(
        max_length=10, choices=SHIFT_CHOICES, default="MORNING"
    )
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    objects = EmployeeManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        team_name = self.team.name if self.team else "No Team"
        return f"{self.first_name} {self.last_name} ({team_name})"
