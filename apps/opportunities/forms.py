"""
opportunities/forms.py
Forms for creating and editing Opportunities and their required skills.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Opportunity, OpportunitySkill


class OpportunityForm(forms.ModelForm):
    """Create / edit an Opportunity posting."""
    class Meta:
        model = Opportunity
        fields = ['title', 'company', 'description', 'location', 'type', 'status', 'salary_range', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Junior Python Developer'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Job description...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Remote / City, Country'}),
            'salary_range': forms.TextInput(attrs={'placeholder': 'e.g. $60k–$80k'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class OpportunitySkillForm(forms.ModelForm):
    """Single required skill row in the formset."""
    class Meta:
        model = OpportunitySkill
        fields = ['skill', 'required_proficiency']


# Inline formset: attach N required skills to one Opportunity
OpportunitySkillFormSet = inlineformset_factory(
    Opportunity,
    OpportunitySkill,
    form=OpportunitySkillForm,
    extra=3,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
