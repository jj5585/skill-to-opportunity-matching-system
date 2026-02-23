"""
matching/models.py
Stores computed MatchResult records for fast retrieval.
"""

from django.db import models
from apps.accounts.models import User
from apps.opportunities.models import Opportunity


class MatchResult(models.Model):
    """
    Cached result of the matching algorithm for a User–Opportunity pair.
    Recalculated whenever skills or opportunity requirements change.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_results')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='match_results')
    match_percentage = models.FloatField(default=0.0)
    matched_skills_count = models.PositiveIntegerField(default=0)
    total_required_skills = models.PositiveIntegerField(default=0)
    missing_skills = models.JSONField(default=list, blank=True)   # List of skill names user is missing
    weak_skills = models.JSONField(default=list, blank=True)      # Skills present but below required level
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'opportunity')
        ordering = ['-match_percentage']
        verbose_name = 'Match Result'

    def __str__(self):
        return f'{self.user.email} ↔ {self.opportunity.title}: {self.match_percentage:.1f}%'
