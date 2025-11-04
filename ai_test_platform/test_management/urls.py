from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TestCaseViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'test-cases', TestCaseViewSet, basename='testcase')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
]