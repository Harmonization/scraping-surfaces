from rest_framework.routers import DefaultRouter
from surface.api.urls import surface_router
from django.urls import path, include

router = DefaultRouter()
router.registry.extend(surface_router.registry)

urlpatterns = [
    path('', include(router.urls))
]
