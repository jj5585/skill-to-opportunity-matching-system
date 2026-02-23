"""SkillSync – Root URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('opportunities/', include('apps.opportunities.urls', namespace='opportunities')),
    path('matching/', include('apps.matching.urls', namespace='matching')),
    # API routes
    path('api/accounts/', include('apps.accounts.api_urls', namespace='api_accounts')),
    path('api/opportunities/', include('apps.opportunities.api_urls', namespace='api_opportunities')),
    path('api/matching/', include('apps.matching.api_urls', namespace='api_matching')),
    # Default redirect
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('dashboard/', include('apps.accounts.dashboard_urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
