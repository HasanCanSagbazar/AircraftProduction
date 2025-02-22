from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UAVSViewSet

router = DefaultRouter()
router.register(r'uavs', UAVSViewSet, basename='uav')

urlpatterns = [
    path('', include(router.urls)),
]
