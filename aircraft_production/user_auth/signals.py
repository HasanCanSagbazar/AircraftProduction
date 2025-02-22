from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import OTP
from django.conf import settings
from users.serializers import EmployeeSerializer


@receiver(post_save, sender=OTP)
def send_otp_email(sender, instance, created, **kwargs):
    """Automatically sends an email when the OTP is generated."""

    if created:
        try:
            employee_data = EmployeeSerializer(instance.employee).data  

            subject = "Your OTP Code"
            message = (
                f"Hello {employee_data['first_name']},\n\n"
                f"Your OTP code is: {instance.code}\n"
                "This code will expire in 5 minutes.\n\n"
                "If you did not request this code, please ignore this email."
            )
            recipient_list = [employee_data['email']]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list
            )

        except Exception as e:
            print(f"Error sending OTP email: {e}")

