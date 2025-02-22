from rest_framework import serializers
from users.serializers import EmployeeSerializer
from users.models import Employee
from .models import OTP
from django.contrib.auth import authenticate
from django.db.models import Q


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email", "role", "phone_number", "team", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

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
        return Employee.objects.create_employee(**validated_data)


class EmployeeLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        # Check employee with the identifier as an email or phone number
        employee = Employee.objects.filter(
            Q(email=identifier) | Q(phone_number=identifier)
        ).first()

        if not employee or not authenticate(username=employee.email, password=password):
            raise serializers.ValidationError("Invalid credentials!")

        # create OTP and save it
        otp = OTPSerializer.create(OTPSerializer(), validated_data={"employee": employee})
        employee_data = EmployeeSerializer(employee).data

        return {"status": True, "data":employee_data, "otp_code": otp.code}


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['employee', 'code']

    def validate_code(self, value):
        """Validate OTP code length and format."""
        if len(value) != 6 or not value.isdigit():
            raise serializers.ValidationError("OTP code must be a 6-digit number.")
        return value

    def validate(self, data):
        """Additional validation to check OTP expiration, usage, and validity."""
        employee = data.get('employee')
        otp_code = data.get('code')

        otp_instance, message = OTP.objects.verify_otp(employee=employee, otp_code=otp_code)
        
        if not otp_instance:
            raise serializers.ValidationError(message)

        tokens = OTP.objects.create_jwt_tokens(employee)
        return tokens

    def create(self, validated_data):
        """Override create method to handle OTP creation using OTPManager."""
        otp = OTP.objects.create_otp(validated_data['employee'])
        return otp


