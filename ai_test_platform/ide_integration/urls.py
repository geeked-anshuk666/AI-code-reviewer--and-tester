from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IDEPluginViewSet, IDEConnectionViewSet, IDEEventViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'plugins', IDEPluginViewSet, basename='ideplugin')
router.register(r'connections', IDEConnectionViewSet, basename='ideconnection')
router.register(r'events', IDEEventViewSet, basename='ideevent')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/ide-integration/', include(router.urls)),
]