"""
opportunities/api_views.py
DRF API views for opportunities and required skills.
"""

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Opportunity, OpportunitySkill
from .serializers import OpportunitySerializer, OpportunitySkillSerializer


class IsRecruiter(permissions.BasePermission):
    """Allow write access only to recruiters."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_recruiter


class OpportunityListCreateAPIView(generics.ListCreateAPIView):
    """GET /api/opportunities/ – list open opportunities; POST – create (recruiter only)."""
    serializer_class = OpportunitySerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        if self.request.user.is_recruiter:
            return Opportunity.objects.filter(recruiter=self.request.user)
        return Opportunity.objects.filter(status='open')

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)


class OpportunityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Opportunity.objects.all()

    def get_object(self):
        obj = super().get_object()
        if self.request.method not in ('GET', 'HEAD', 'OPTIONS'):
            if obj.recruiter != self.request.user:
                raise PermissionDenied('You do not own this opportunity.')
        return obj


class OpportunitySkillListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OpportunitySkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OpportunitySkill.objects.filter(opportunity_id=self.kwargs['opp_pk'])

    def perform_create(self, serializer):
        opp = Opportunity.objects.get(pk=self.kwargs['opp_pk'], recruiter=self.request.user)
        serializer.save(opportunity=opp)
