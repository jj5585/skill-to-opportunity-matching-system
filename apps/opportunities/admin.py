from django.contrib import admin
from .models import Opportunity, OpportunitySkill

class OpportunitySkillInline(admin.TabularInline):
    model = OpportunitySkill
    extra = 2

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'type', 'status', 'recruiter', 'created_at']
    list_filter = ['type', 'status']
    inlines = [OpportunitySkillInline]
