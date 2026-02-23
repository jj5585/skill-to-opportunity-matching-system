"""
accounts/models.py
Defines the custom User model, Profile, Skill, and UserSkill.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended user model with role-based access.
    Roles: user (job-seeker/student), recruiter, admin.
    Password hashing is handled automatically by AbstractUser.
    """
    ROLE_USER = 'user'
    ROLE_RECRUITER = 'recruiter'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, 'Job Seeker / Student'),
        (ROLE_RECRUITER, 'Recruiter'),
        (ROLE_ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email} ({self.role})'

    # ── Role helpers ──────────────────────────────────────────────────────────
    @property
    def is_recruiter(self):
        return self.role == self.ROLE_RECRUITER

    @property
    def is_job_seeker(self):
        return self.role == self.ROLE_USER

    @property
    def is_site_admin(self):
        return self.role == self.ROLE_ADMIN


class Profile(models.Model):
    """One-to-one extension of User with personal/professional details."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.email}'


class Skill(models.Model):
    """
    Master list of skills (shared reference table).
    E.g. Python, React, Communication, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True, help_text='e.g. Programming, Design, Soft Skills')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    Junction table linking a User to a Skill with a proficiency level.
    Proficiency scoring: Beginner=1, Intermediate=2, Advanced=3
    """
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

    PROFICIENCY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    PROFICIENCY_SCORE = {
        BEGINNER: 1,
        INTERMEDIATE: 2,
        ADVANCED: 3,
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default=BEGINNER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')  # Each user can have each skill only once
        verbose_name = 'User Skill'

    def __str__(self):
        return f'{self.user.email} – {self.skill.name} ({self.proficiency})'

    @property
    def score(self):
        """Return the numeric score for this proficiency level."""
        return self.PROFICIENCY_SCORE.get(self.proficiency, 0)
