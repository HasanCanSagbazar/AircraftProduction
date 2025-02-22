# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UavsAssemblyViewSet, AssemblyPartViewSet

router = DefaultRouter()
router.register(r'assemblies', UavsAssemblyViewSet)
router.register(r'assembly-parts', AssemblyPartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
