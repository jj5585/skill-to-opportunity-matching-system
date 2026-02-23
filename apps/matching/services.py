"""
matching/services.py
─────────────────────────────────────────────────────────────────────────────
SkillSync Matching Engine
─────────────────────────────────────────────────────────────────────────────
Algorithm:
  Proficiency scores  →  Beginner=1  |  Intermediate=2  |  Advanced=3

  For each required skill in an opportunity:
    • User proficiency >= required  →  full score  (required_score)
    • User proficiency <  required  →  half score  (required_score / 2)
    • Skill not present             →  0

  match % = (user_total_score / max_possible_score) × 100
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from apps.accounts.models import UserSkill
from apps.opportunities.models import Opportunity, OpportunitySkill


# ── Proficiency score map ────────────────────────────────────────────────────
PROF_SCORE: dict[str, int] = {
    'beginner': 1,
    'intermediate': 2,
    'advanced': 3,
}


@dataclass
class SkillMatchDetail:
    """Breakdown for a single required skill."""
    skill_name: str
    required_proficiency: str
    user_proficiency: str | None   # None → skill absent
    required_score: int
    earned_score: float
    status: str  # 'full' | 'partial' | 'missing'


@dataclass
class MatchReport:
    """Full match result for one User ↔ Opportunity pair."""
    user_id: int
    opportunity_id: int
    match_percentage: float
    user_score: float
    max_possible_score: int
    matched_skills_count: int
    total_required_skills: int
    missing_skills: List[str] = field(default_factory=list)
    weak_skills: List[str] = field(default_factory=list)
    details: List[SkillMatchDetail] = field(default_factory=list)


def compute_match(user, opportunity: Opportunity) -> MatchReport:
    """
    Compute a MatchReport for a single user–opportunity pair.

    Parameters
    ----------
    user        : accounts.User instance
    opportunity : opportunities.Opportunity instance

    Returns
    -------
    MatchReport dataclass with full breakdown.
    """

    # Build a lookup dict:  skill_id → proficiency string
    user_skill_map: dict[int, str] = {
        us.skill_id: us.proficiency
        for us in UserSkill.objects.filter(user=user).select_related('skill')
    }

    required_skills: list[OpportunitySkill] = list(
        opportunity.required_skills.select_related('skill').all()
    )

    total_required = len(required_skills)

    if total_required == 0:
        # No skills required → instant 100% match
        return MatchReport(
            user_id=user.pk,
            opportunity_id=opportunity.pk,
            match_percentage=100.0,
            user_score=0,
            max_possible_score=0,
            matched_skills_count=0,
            total_required_skills=0,
        )

    max_possible_score: int = 0
    user_total_score: float = 0.0
    missing_skills: list[str] = []
    weak_skills: list[str] = []
    details: list[SkillMatchDetail] = []
    matched_count: int = 0

    for opp_skill in required_skills:
        skill_name = opp_skill.skill.name
        req_prof = opp_skill.required_proficiency
        req_score = PROF_SCORE[req_prof]
        max_possible_score += req_score

        user_prof = user_skill_map.get(opp_skill.skill_id)

        if user_prof is None:
            # Skill completely absent
            earned = 0.0
            status = 'missing'
            missing_skills.append(skill_name)
        else:
            user_score_val = PROF_SCORE[user_prof]
            if user_score_val >= req_score:
                # Full score
                earned = float(req_score)
                status = 'full'
                matched_count += 1
            else:
                # Partial: half of required score
                earned = req_score / 2.0
                status = 'partial'
                weak_skills.append(skill_name)

        user_total_score += earned

        details.append(SkillMatchDetail(
            skill_name=skill_name,
            required_proficiency=req_prof,
            user_proficiency=user_prof,
            required_score=req_score,
            earned_score=earned,
            status=status,
        ))

    # Compute percentage, guard against division by zero
    percentage = (user_total_score / max_possible_score) * 100 if max_possible_score > 0 else 0.0

    return MatchReport(
        user_id=user.pk,
        opportunity_id=opportunity.pk,
        match_percentage=round(percentage, 2),
        user_score=user_total_score,
        max_possible_score=max_possible_score,
        matched_skills_count=matched_count,
        total_required_skills=total_required,
        missing_skills=missing_skills,
        weak_skills=weak_skills,
        details=details,
    )


def compute_and_save_match(user, opportunity: Opportunity):
    """
    Compute match and persist/update a MatchResult record.
    Returns the saved MatchResult instance.
    """
    from apps.matching.models import MatchResult

    report = compute_match(user, opportunity)

    result, _ = MatchResult.objects.update_or_create(
        user=user,
        opportunity=opportunity,
        defaults={
            'match_percentage': report.match_percentage,
            'matched_skills_count': report.matched_skills_count,
            'total_required_skills': report.total_required_skills,
            'missing_skills': report.missing_skills,
            'weak_skills': report.weak_skills,
        }
    )
    return result


def get_top_opportunities_for_user(user, limit: int = 20):
    """
    Compute and return top-matched opportunities for a given user,
    sorted by match percentage descending.
    Returns list of MatchReport objects.
    """
    from apps.opportunities.models import Opportunity

    opportunities = Opportunity.objects.filter(status='open').prefetch_related(
        'required_skills__skill'
    )

    reports = [compute_match(user, opp) for opp in opportunities]
    reports.sort(key=lambda r: r.match_percentage, reverse=True)
    return reports[:limit]


def get_top_candidates_for_opportunity(opportunity: Opportunity, limit: int = 50):
    """
    Compute and return top-matched users for a given opportunity,
    sorted by match percentage descending.
    Returns list of MatchReport objects.
    """
    from apps.accounts.models import User

    candidates = User.objects.filter(role='user').prefetch_related('user_skills__skill')

    reports = [compute_match(user, opportunity) for user in candidates]
    reports.sort(key=lambda r: r.match_percentage, reverse=True)
    return reports[:limit]
