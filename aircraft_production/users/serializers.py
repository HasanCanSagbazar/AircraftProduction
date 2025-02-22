from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'position', 'team', 'date_of_birth', 'shift']
        read_only_fields = ["id", "is_active", "last_login", "created_at", "updated_at"]


    def validate_email(self, value):
        """Check if the email already exists"""
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value


    def validate_phone_number(self, value):
        """Check if the phone number already exists"""
        if Employee.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


    def create(self, validated_data):
        """Use custom Manager to create an employee"""
        return Employee.create_employee(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            team=validated_data["team"],
            position=validated_data["position"],
            shift=validated_data.get("shift", "MORNING"),
            date_of_birth=validated_data.get("date_of_birth", None),
        )
    

    def update(self, instance, validated_data):
        """Override update method to only update specific fields."""
        for field in ['first_name', 'last_name', 'position', 'shift', 'team', 'email', 'phone_number', 'date_of_birth']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
            else:
                continue
        instance.save()
        return instance
