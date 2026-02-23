"""
matching/serializers.py
DRF serializers for MatchResult.
"""

from rest_framework import serializers
from .models import MatchResult


class MatchResultSerializer(serializers.ModelSerializer):
    opportunity_title = serializers.CharField(source='opportunity.title', read_only=True)
    opportunity_company = serializers.CharField(source='opportunity.company', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = MatchResult
        fields = [
            'id', 'user', 'user_email', 'opportunity', 'opportunity_title',
            'opportunity_company', 'match_percentage', 'matched_skills_count',
            'total_required_skills', 'missing_skills', 'weak_skills', 'computed_at',
        ]
        read_only_fields = fields
