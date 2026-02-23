"""
matching/views.py
Views for the matching engine results.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.matching.services import get_top_opportunities_for_user, compute_match
from apps.opportunities.models import Opportunity


class MyMatchesView(LoginRequiredMixin, View):
    """Show all matched opportunities for the currently logged-in job seeker."""
    template_name = 'matching/my_matches.html'

    def get(self, request):
        matches = get_top_opportunities_for_user(request.user, limit=50)
        # Filter by minimum match %
        min_pct = int(request.GET.get('min', 0))
        if min_pct:
            matches = [m for m in matches if m.match_percentage >= min_pct]

        context = {
            'matches': matches,
            'min_pct': min_pct,
            'total': len(matches),
        }
        return render(request, self.template_name, context)


class MatchDetailView(LoginRequiredMixin, View):
    """Detailed skill-by-skill breakdown for a specific opportunity match."""
    template_name = 'matching/match_detail.html'

    def get(self, request, opportunity_pk):
        opp = get_object_or_404(Opportunity, pk=opportunity_pk)
        report = compute_match(request.user, opp)
        context = {
            'opportunity': opp,
            'report': report,
        }
        return render(request, self.template_name, context)
