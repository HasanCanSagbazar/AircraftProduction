from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartProductionViewSet

router = DefaultRouter()
router.register(r'production', PartProductionViewSet, basename='uav')

urlpatterns = [
    path('', include(router.urls)),
]
