"""
opportunities/models.py
Defines Opportunity and OpportunitySkill models.
"""

from django.db import models
from apps.accounts.models import User, Skill, UserSkill


class Opportunity(models.Model):
    """
    A job, internship, or project posted by a Recruiter.
    """
    TYPE_JOB = 'job'
    TYPE_INTERNSHIP = 'internship'
    TYPE_PROJECT = 'project'

    TYPE_CHOICES = [
        (TYPE_JOB, 'Full-Time Job'),
        (TYPE_INTERNSHIP, 'Internship'),
        (TYPE_PROJECT, 'Project'),
    ]

    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]

    recruiter = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posted_opportunities',
        limit_choices_to={'role': 'recruiter'}
    )
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_JOB)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    salary_range = models.CharField(max_length=100, blank=True, help_text='e.g. $60k–$80k')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Opportunities'

    def __str__(self):
        return f'{self.title} @ {self.company}'

    @property
    def max_possible_score(self):
        """Sum of maximum scores for all required skills."""
        return sum(
            UserSkill.PROFICIENCY_SCORE[opp_skill.required_proficiency]
            for opp_skill in self.required_skills.all()
        )


class OpportunitySkill(models.Model):
    """
    Junction table: which skills (and minimum proficiency) an Opportunity requires.
    """
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE,
        related_name='required_skills'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='opportunity_skills')
    required_proficiency = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )

    class Meta:
        unique_together = ('opportunity', 'skill')
        verbose_name = 'Required Skill'

    def __str__(self):
        return f'{self.opportunity.title} requires {self.skill.name} ({self.required_proficiency})'
