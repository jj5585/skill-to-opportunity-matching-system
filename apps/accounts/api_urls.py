"""accounts/api_urls.py"""

from django.urls import path
from .api_views import RegisterAPIView, MeAPIView, SkillListAPIView, UserSkillListCreateAPIView, UserSkillDetailAPIView

app_name = 'api_accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('skills/', SkillListAPIView.as_view(), name='skills'),
    path('my-skills/', UserSkillListCreateAPIView.as_view(), name='my_skills'),
    path('my-skills/<int:pk>/', UserSkillDetailAPIView.as_view(), name='my_skill_detail'),
]
