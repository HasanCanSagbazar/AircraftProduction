from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.utils.timezone import now
import random


class OTPManager(models.Manager):
    OTP_STATUS = {
        'valid': 'OTP is valid.',
        'expired': 'OTP has expired.',
        'used': 'OTP has already been used.',
        'invalid': 'Invalid OTP code.',
    }


    def create_otp(self, employee):
        """Creates a new OTP for the specified employee manually."""
        code = str(random.randint(100000, 999999))
        otp = self.model(employee=employee, code=code)
        otp.save(using=self._db)
        return otp


    def verify_otp(self, employee, otp_code):
        """Checks the validity of the OTP and whether it is still valid."""
        otp_instance = self.filter(employee=employee, code=otp_code, is_used=False).first()

        if not otp_instance:
            return None, self.OTP_STATUS['invalid']

        if otp_instance.is_used:
            return None, self.OTP_STATUS['used']

        if not otp_instance.is_valid():
            return None, self.OTP_STATUS['expired']

        # Mark the OTP as used
        otp_instance.mark_used()
        return otp_instance, self.OTP_STATUS['valid']
    
    
    def create_jwt_tokens(self, employee):
        """Create JWT tokens upon successful OTP verification."""
        refresh = RefreshToken.for_user(employee)
        team = str(employee.team.id)
        refresh.payload['team'] = team
        access_token = str(refresh.access_token)
        
        return {"access_token": access_token, "refresh_token": str(refresh)}
    
