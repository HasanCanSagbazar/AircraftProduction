from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeLoginViewSet, EmployeeRegisterViewSet, OTPVerifyViewSet

router = DefaultRouter()
router.register(r'login', EmployeeLoginViewSet, basename='login')
router.register(r'register', EmployeeRegisterViewSet, basename='register')
router.register(r'verify-otp', OTPVerifyViewSet, basename='verify-otp')

urlpatterns = [
    path('auth/', include(router.urls)),
]
