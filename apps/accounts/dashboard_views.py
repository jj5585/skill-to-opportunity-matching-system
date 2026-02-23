"""
accounts/dashboard_views.py
Central dashboard – redirects based on user role.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.matching.services import get_top_opportunities_for_user
from apps.opportunities.models import Opportunity
from apps.matching.models import MatchResult


class DashboardView(LoginRequiredMixin, View):
    """
    Role-aware dashboard:
    • Job seekers → see top matched opportunities
    • Recruiters  → see their posted opportunities & candidate stats
    • Admins      → redirect to Django admin
    """

    def get(self, request):
        user = request.user

        if user.is_recruiter:
            return self._recruiter_dashboard(request)
        elif user.is_site_admin:
            from django.shortcuts import redirect
            return redirect('/admin/')
        else:
            return self._user_dashboard(request)

    def _user_dashboard(self, request):
        """Dashboard for job seekers / students."""
        user = request.user

        # Compute live matches for the top 10 opportunities
        top_matches = get_top_opportunities_for_user(user, limit=10)

        # Stats
        skills_count = user.user_skills.count()
        match_count = len([m for m in top_matches if m.match_percentage > 0])

        context = {
            'top_matches': top_matches,
            'skills_count': skills_count,
            'match_count': match_count,
            'open_opportunities': Opportunity.objects.filter(status='open').count(),
        }
        return render(request, 'dashboard/user_dashboard.html', context)

    def _recruiter_dashboard(self, request):
        """Dashboard for recruiters."""
        user = request.user

        my_opportunities = Opportunity.objects.filter(recruiter=user).prefetch_related(
            'required_skills__skill'
        )

        context = {
            'my_opportunities': my_opportunities,
            'total_posted': my_opportunities.count(),
            'total_open': my_opportunities.filter(status='open').count(),
        }
        return render(request, 'dashboard/recruiter_dashboard.html', context)
