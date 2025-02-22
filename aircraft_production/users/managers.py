from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

class EmployeeManager(BaseUserManager):

    def create_employee(self, **kwargs):
        """Create method for an employee"""
        kwargs["password"] = make_password(kwargs["password"])
        employee = self.model(**kwargs)
        employee.save(using=self._db)
        return employee
    
    def all_employees(self):
        """Get all employees (can add additional filtering logic if needed)"""
        return self.all()

    def create_superuser(self, email, password=None, **extra_fields):
        """Create method for a superuser"""
        if not email:
            raise ValueError("Superuser must have an email address")
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_employee(email=email, password=password, **extra_fields)

    def get_by_natural_key(self, username):
        """Allow Django to retrieve users by their email instead of username"""
        return self.get(email=username)
