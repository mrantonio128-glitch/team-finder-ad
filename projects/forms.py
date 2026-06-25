"""Projects forms."""

from django import forms

from core.forms import GithubUrlValidationMixin
from projects.models import Project


class ProjectForm(GithubUrlValidationMixin, forms.ModelForm):
    """Project create / edit form."""

    class Meta:
        model = Project
        fields = ("name", "description", "github_url")
        labels = {
            "name": "Название проекта",
            "description": "Описание проекта",
            "github_url": "Ссылка на Github",
        }
