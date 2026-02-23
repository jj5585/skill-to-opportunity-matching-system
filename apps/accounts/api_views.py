"""
accounts/api_views.py
DRF API views for user registration, profile, and skills.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Skill, UserSkill
from .serializers import RegisterSerializer, UserSerializer, SkillSerializer, UserSkillSerializer


class RegisterAPIView(generics.CreateAPIView):
    """POST /api/accounts/register/ – create a new user account."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/accounts/me/ – current user profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SkillListAPIView(generics.ListCreateAPIView):
    """GET /api/accounts/skills/ – list all master skills."""
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserSkillListCreateAPIView(generics.ListCreateAPIView):
    """GET/POST /api/accounts/my-skills/ – list or add user skills."""
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_skills.select_related('skill').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/accounts/my-skills/<pk>/"""
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_skills.all()
