from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestExecutionViewSet, TestResultViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'executions', TestExecutionViewSet, basename='testexecution')
router.register(r'results', TestResultViewSet, basename='testresult')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/test-execution/', include(router.urls)),
]