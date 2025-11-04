from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, DashboardViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'dashboards', DashboardViewSet, basename='dashboard')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/reporting/', include(router.urls)),
]