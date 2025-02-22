from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamsViewSet

router = DefaultRouter()
router.register(r'teams', TeamsViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]
