"""
accounts/forms.py
Django forms for registration, login, profile editing, and skill management.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Profile, UserSkill, Skill


class RegisterForm(forms.ModelForm):
    """Registration form with password confirmation and role selection."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Min 8 characters'}),
        min_length=8,
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password', 'password_confirm']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    """Custom login form using email instead of username."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'autofocus': True}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )


class ProfileForm(forms.ModelForm):
    """Edit Profile details."""
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'phone', 'linkedin_url', 'github_url', 'portfolio_url', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 555 000 0000'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/...'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
        }


class UserSkillForm(forms.ModelForm):
    """Add a skill with proficiency level to the current user."""
    class Meta:
        model = UserSkill
        fields = ['skill', 'proficiency']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            # Exclude skills the user already has
            existing = user.user_skills.values_list('skill_id', flat=True)
            self.fields['skill'].queryset = Skill.objects.exclude(id__in=existing)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
