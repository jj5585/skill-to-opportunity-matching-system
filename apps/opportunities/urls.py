"""opportunities/urls.py"""

from django.urls import path
from .views import (
    OpportunityListView, OpportunityDetailView,
    OpportunityCreateView, OpportunityEditView, OpportunityDeleteView,
    RecruiterCandidatesView,
)

app_name = 'opportunities'

urlpatterns = [
    path('', OpportunityListView.as_view(), name='list'),
    path('<int:pk>/', OpportunityDetailView.as_view(), name='detail'),
    path('create/', OpportunityCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', OpportunityEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', OpportunityDeleteView.as_view(), name='delete'),
    path('<int:pk>/candidates/', RecruiterCandidatesView.as_view(), name='candidates'),
]
