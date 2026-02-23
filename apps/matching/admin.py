from django.contrib import admin
from .models import MatchResult

@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'opportunity', 'match_percentage', 'computed_at']
    list_filter = ['match_percentage']
    ordering = ['-match_percentage']
