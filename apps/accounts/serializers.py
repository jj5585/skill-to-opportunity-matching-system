"""
accounts/serializers.py
DRF serializers for User, Profile, Skill, UserSkill.
"""

from rest_framework import serializers
from .models import User, Profile, Skill, UserSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description']


class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_name', 'skill_category', 'proficiency', 'score']
        read_only_fields = ['score']

    def validate(self, data):
        # Prevent duplicate user-skill via API
        user = self.context['request'].user
        skill = data.get('skill')
        if self.instance is None and UserSkill.objects.filter(user=user, skill=skill).exists():
            raise serializers.ValidationError('You have already added this skill.')
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'phone', 'linkedin_url', 'github_url', 'portfolio_url', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    user_skills = UserSkillSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'profile', 'user_skills']
        read_only_fields = ['role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)   # Hashes via PBKDF2
        user.save()
        Profile.objects.create(user=user)
        return user
