"""accounts/dashboard_urls.py"""

from django.urls import path
from .dashboard_views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
]
