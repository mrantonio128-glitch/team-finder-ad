"""Project's admin defs."""

from django.contrib import admin

from projects import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Projects."""

    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "owner__email", "description")

    readonly_fields = ("created_at",)

    filter_horizontal = ("participants",)

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "owner", "status")},
        ),
        ("Links", {"fields": ("github_url",)}),
        ("Project Team", {"fields": ("participants",)}),
        ("Dates", {"fields": ("created_at",)}),
    )
