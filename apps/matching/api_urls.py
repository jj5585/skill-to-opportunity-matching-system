"""matching/api_urls.py"""

from django.urls import path
from .api_views import MyMatchesAPIView, OpportunityCandidatesAPIView

app_name = 'api_matching'

urlpatterns = [
    path('my-matches/', MyMatchesAPIView.as_view(), name='my_matches'),
    path('candidates/<int:opp_pk>/', OpportunityCandidatesAPIView.as_view(), name='candidates'),
]
