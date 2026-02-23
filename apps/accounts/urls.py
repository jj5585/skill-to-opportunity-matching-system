"""accounts/urls.py – HTML view routes"""

from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, ProfileEditView,
    UserSkillListView, UserSkillAddView, UserSkillDeleteView, UserSkillUpdateView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('skills/', UserSkillListView.as_view(), name='skills'),
    path('skills/add/', UserSkillAddView.as_view(), name='skill_add'),
    path('skills/<int:pk>/delete/', UserSkillDeleteView.as_view(), name='skill_delete'),
    path('skills/<int:pk>/update/', UserSkillUpdateView.as_view(), name='skill_update'),
]
