"""opportunities/api_urls.py"""

from django.urls import path
from .api_views import OpportunityListCreateAPIView, OpportunityDetailAPIView, OpportunitySkillListCreateAPIView

app_name = 'api_opportunities'

urlpatterns = [
    path('', OpportunityListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', OpportunityDetailAPIView.as_view(), name='detail'),
    path('<int:opp_pk>/skills/', OpportunitySkillListCreateAPIView.as_view(), name='skills'),
]
