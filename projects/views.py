"""Project views."""

from typing import Any
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.constants import (
    API_STATUS_ERR,
    API_STATUS_OK,
    ERR_MSG_ACTION_NOT_ALLOWED,
    PROJECTS_PAGINATE_BY,
)
from projects.forms import ProjectForm
from projects.mixins import IsOwnerMixin
from projects.models import Project


def index_redirect(request: HttpRequest) -> HttpResponse:
    """Root redirect to projects list."""
    return redirect("projects:list")


class ProjectListView(ListView):
    """Project list view."""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PAGINATE_BY

    def get_queryset(self) -> QuerySet[Project]:
        """Sort newest."""
        return (
            Project.objects.select_related("owner")
            .prefetch_related("participants")
            .order_by("-created_at")
        )


class ProjectDetailView(DetailView):
    """Project details view."""

    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Project create view."""

    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs: Any) -> dict:
        """Set template as not edit."""
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form: ProjectForm) -> HttpResponse:
        """Form validation."""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # add author to contributors
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self) -> str:
        """Redirect to created project once done."""
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    """Project update view."""

    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs: Any) -> dict:
        """Set template as yes edit."""
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

    def get_success_url(self) -> str:
        """Redirect to created project once done."""
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


@login_required
@require_POST
def toggle_favorite(request: HttpRequest, pk: int) -> JsonResponse:
    """Add or remove project from favorites."""
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return JsonResponse(
            {"status": API_STATUS_ERR, "message": "Project not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    user = request.user

    if was_favorited := user.favorites.filter(pk=project.pk).exists():
        user.favorites.remove(project)
    else:
        user.favorites.add(project)

    return JsonResponse({"status": API_STATUS_OK, "favorited": not was_favorited})


@login_required
@require_POST
def complete_project(request: HttpRequest, pk: int) -> JsonResponse:
    """Close project if user is owner."""
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return JsonResponse(
            {"status": API_STATUS_ERR, "message": "Project not found"},
            status=HTTPStatus.NOT_FOUND,
        )

    if request.user == project.owner and project.status == Project.Status.OPEN:
        project.status = Project.Status.CLOSED
        project.save(update_fields=["status"])
        return JsonResponse(
            {
                "status": API_STATUS_OK,
                "project_status": Project.Status.CLOSED.value,
            }
        )

    return JsonResponse(
        {"status": API_STATUS_ERR, "message": ERR_MSG_ACTION_NOT_ALLOWED},
        status=HTTPStatus.FORBIDDEN,
    )


@login_required
@require_POST
def toggle_participate(request: HttpRequest, pk: int) -> JsonResponse:
    """Join or leave the project."""
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return JsonResponse(
            {"status": API_STATUS_ERR, "message": "Project not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    user = request.user

    if was_participant := project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
    else:
        project.participants.add(user)

    return JsonResponse({"status": API_STATUS_OK, "participant": not was_participant})


class FavoriteProjectsListView(LoginRequiredMixin, ListView):
    """Favorite projects page."""

    model = Project
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PAGINATE_BY

    def get_queryset(self) -> QuerySet:
        """Get only favorites."""
        return (
            self.request.user.favorites.select_related("owner")
            .prefetch_related("participants")
            .order_by("-created_at")
        )
