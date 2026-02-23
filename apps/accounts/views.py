"""
accounts/views.py
Class-based views for registration, login, logout, profile management, and skill CRUD.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm, UserSkillForm
from .models import Profile, UserSkill, Skill


# ── Authentication Views ───────────────────────────────────────────────────────

class RegisterView(View):
    """Handle user registration with role selection."""
    template_name = 'accounts/register.html'

    def get(self, request):
        from django.shortcuts import render
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        from django.shortcuts import render
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.email}! Account created successfully.')
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Handle email/password login."""
    template_name = 'accounts/login.html'

    def get(self, request):
        from django.shortcuts import render
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        from django.shortcuts import render
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}!')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Log out and redirect to login page."""
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('accounts:login')


# ── Profile Views ──────────────────────────────────────────────────────────────

class ProfileView(LoginRequiredMixin, TemplateView):
    """View own profile."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = getattr(self.request.user, 'profile', None)
        ctx['user_skills'] = self.request.user.user_skills.select_related('skill').all()
        return ctx


class ProfileEditView(LoginRequiredMixin, View):
    """Edit profile details."""
    template_name = 'accounts/profile_edit.html'

    def _get_profile(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return profile

    def get(self, request):
        from django.shortcuts import render
        form = ProfileForm(instance=self._get_profile(request))
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        from django.shortcuts import render
        form = ProfileForm(request.POST, request.FILES, instance=self._get_profile(request))
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})


# ── Skill Management Views ─────────────────────────────────────────────────────

class UserSkillListView(LoginRequiredMixin, TemplateView):
    """List user's skills; provide form to add a new one."""
    template_name = 'accounts/skills.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_skills'] = self.request.user.user_skills.select_related('skill').all()
        ctx['form'] = UserSkillForm(user=self.request.user)
        return ctx


class UserSkillAddView(LoginRequiredMixin, View):
    """Add a skill to the current user."""
    def post(self, request):
        form = UserSkillForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added successfully.')
        else:
            messages.error(request, 'Could not add skill. Please check the form.')
        return redirect('accounts:skills')


class UserSkillDeleteView(LoginRequiredMixin, View):
    """Remove a skill from the current user."""
    def post(self, request, pk):
        try:
            skill = request.user.user_skills.get(pk=pk)
            skill.delete()
            messages.success(request, 'Skill removed.')
        except UserSkill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        return redirect('accounts:skills')


class UserSkillUpdateView(LoginRequiredMixin, View):
    """Update proficiency for an existing user skill."""
    def post(self, request, pk):
        from django.shortcuts import render
        try:
            user_skill = request.user.user_skills.get(pk=pk)
            proficiency = request.POST.get('proficiency')
            valid = [c[0] for c in UserSkill.PROFICIENCY_CHOICES]
            if proficiency in valid:
                user_skill.proficiency = proficiency
                user_skill.save()
                messages.success(request, f'Updated {user_skill.skill.name} proficiency.')
            else:
                messages.error(request, 'Invalid proficiency level.')
        except UserSkill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        return redirect('accounts:skills')
