"""
matching/api_views.py
DRF API views for the matching engine.
"""

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.matching.services import get_top_opportunities_for_user, get_top_candidates_for_opportunity
from apps.opportunities.models import Opportunity


class MyMatchesAPIView(APIView):
    """GET /api/matching/my-matches/ – top opportunities for the logged-in user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = get_top_opportunities_for_user(request.user, limit=50)
        data = [
            {
                'opportunity_id': r.opportunity_id,
                'match_percentage': r.match_percentage,
                'matched_skills_count': r.matched_skills_count,
                'total_required_skills': r.total_required_skills,
                'missing_skills': r.missing_skills,
                'weak_skills': r.weak_skills,
            }
            for r in reports
        ]
        return Response(data)


class OpportunityCandidatesAPIView(APIView):
    """GET /api/matching/candidates/<opp_pk>/ – ranked candidates for recruiter."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, opp_pk):
        opp = Opportunity.objects.get(pk=opp_pk, recruiter=request.user)
        reports = get_top_candidates_for_opportunity(opp, limit=50)
        data = [
            {
                'user_id': r.user_id,
                'match_percentage': r.match_percentage,
                'matched_skills_count': r.matched_skills_count,
                'total_required_skills': r.total_required_skills,
                'missing_skills': r.missing_skills,
            }
            for r in reports
        ]
        return Response(data)
