"""
opportunities/views.py
Class-based views for listing, creating, editing, and deleting Opportunities.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Opportunity, OpportunitySkill
from .forms import OpportunityForm, OpportunitySkillFormSet
from apps.matching.services import get_top_candidates_for_opportunity, compute_match


class OpportunityListView(LoginRequiredMixin, ListView):
    """Public opportunity board – all open opportunities."""
    model = Opportunity
    template_name = 'opportunities/list.html'
    context_object_name = 'opportunities'
    paginate_by = 12

    def get_queryset(self):
        qs = Opportunity.objects.filter(status='open').prefetch_related('required_skills__skill')
        q = self.request.GET.get('q')
        opp_type = self.request.GET.get('type')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(company__icontains=q)
        if opp_type:
            qs = qs.filter(type=opp_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['type_choices'] = Opportunity.TYPE_CHOICES
        ctx['selected_type'] = self.request.GET.get('type', '')
        ctx['search_q'] = self.request.GET.get('q', '')
        return ctx


class OpportunityDetailView(LoginRequiredMixin, View):
    """Detail page: show opportunity info + match result for current user."""
    template_name = 'opportunities/detail.html'

    def get(self, request, pk):
        opp = get_object_or_404(Opportunity, pk=pk)
        match_report = None
        if request.user.is_job_seeker:
            match_report = compute_match(request.user, opp)
        context = {
            'opportunity': opp,
            'required_skills': opp.required_skills.select_related('skill').all(),
            'match_report': match_report,
        }
        return render(request, self.template_name, context)


class OpportunityCreateView(LoginRequiredMixin, View):
    """Recruiter: create a new opportunity with required skills."""
    template_name = 'opportunities/form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_recruiter:
            messages.error(request, 'Only recruiters can post opportunities.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = OpportunityForm()
        formset = OpportunitySkillFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset, 'action': 'Create'})

    def post(self, request):
        form = OpportunityForm(request.POST)
        formset = OpportunitySkillFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            opp = form.save(commit=False)
            opp.recruiter = request.user
            opp.save()
            formset.instance = opp
            formset.save()
            messages.success(request, f'Opportunity "{opp.title}" created successfully.')
            return redirect('opportunities:detail', pk=opp.pk)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'action': 'Create'})


class OpportunityEditView(LoginRequiredMixin, View):
    """Recruiter: edit an existing opportunity."""
    template_name = 'opportunities/form.html'

    def _get_opportunity(self, request, pk):
        return get_object_or_404(Opportunity, pk=pk, recruiter=request.user)

    def get(self, request, pk):
        opp = self._get_opportunity(request, pk)
        form = OpportunityForm(instance=opp)
        formset = OpportunitySkillFormSet(instance=opp)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'action': 'Edit', 'opportunity': opp})

    def post(self, request, pk):
        opp = self._get_opportunity(request, pk)
        form = OpportunityForm(request.POST, instance=opp)
        formset = OpportunitySkillFormSet(request.POST, instance=opp)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Opportunity updated.')
            return redirect('opportunities:detail', pk=opp.pk)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'action': 'Edit', 'opportunity': opp})


class OpportunityDeleteView(LoginRequiredMixin, View):
    """Recruiter: delete an opportunity."""
    def post(self, request, pk):
        opp = get_object_or_404(Opportunity, pk=pk, recruiter=request.user)
        opp.delete()
        messages.success(request, 'Opportunity deleted.')
        return redirect('dashboard:home')


class RecruiterCandidatesView(LoginRequiredMixin, View):
    """Recruiter: view ranked candidate matches for an opportunity."""
    template_name = 'opportunities/candidates.html'

    def get(self, request, pk):
        opp = get_object_or_404(Opportunity, pk=pk, recruiter=request.user)
        candidates = get_top_candidates_for_opportunity(opp, limit=50)
        context = {
            'opportunity': opp,
            'candidates': candidates,
        }
        return render(request, self.template_name, context)
