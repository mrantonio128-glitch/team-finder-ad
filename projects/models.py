"""Project models."""

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.models import GithubLinkMixin
from projects.constants import PROJECT_NAME_MAX_LENGTH, PROJECT_STATUS_MAX_LENGTH


class Project(GithubLinkMixin):
    """Project model."""

    class Status(models.TextChoices):
        OPEN = "open", "Открыт"
        CLOSED = "closed", "Закрыт"

    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_projects",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,  # bruuuh
        choices=Status.choices,
        default=Status.OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
    )

    def __str__(self) -> str:
        """String representation of project (its name)."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Canonical project url."""
        return reverse("projects:detail", kwargs={"pk": self.pk})
