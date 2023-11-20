from rest_framework.routers import DefaultRouter
from .views import SurfaceViewSet

surface_router = DefaultRouter()
surface_router.register(r'surface', SurfaceViewSet)