"""
opportunities/serializers.py
DRF serializers for Opportunity and OpportunitySkill.
"""

from rest_framework import serializers
from .models import Opportunity, OpportunitySkill
from apps.accounts.serializers import SkillSerializer


class OpportunitySkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = OpportunitySkill
        fields = ['id', 'skill', 'skill_name', 'required_proficiency']


class OpportunitySerializer(serializers.ModelSerializer):
    required_skills = OpportunitySkillSerializer(many=True, read_only=True)
    recruiter_email = serializers.EmailField(source='recruiter.email', read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'company', 'description', 'location',
            'type', 'status', 'salary_range', 'deadline',
            'recruiter', 'recruiter_email', 'required_skills',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['recruiter', 'recruiter_email']

    def create(self, validated_data):
        validated_data['recruiter'] = self.context['request'].user
        return super().create(validated_data)
