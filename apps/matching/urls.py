"""matching/urls.py"""

from django.urls import path
from .views import MyMatchesView, MatchDetailView

app_name = 'matching'

urlpatterns = [
    path('my-matches/', MyMatchesView.as_view(), name='my_matches'),
    path('opportunity/<int:opportunity_pk>/', MatchDetailView.as_view(), name='match_detail'),
]
