from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartViewSet

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='uav')

urlpatterns = [
    path('', include(router.urls)),
]
