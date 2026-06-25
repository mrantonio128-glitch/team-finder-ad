from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts import forms

UserModel = get_user_model()


BASIC_FIELDSET = (
    None,
    {
        "fields": (
            "email",
            "password",
        )
    },
)

PERSONAL_INFO_FIELDSET = (
    "Personal Info",
    {
        "fields": (
            "name",
            "surname",
            "avatar",
            "phone",
            "about",
            "github_url",
        )
    },
)

PERMISSIONS_FIELDSET = (
    "Permissions",
    {
        "fields": (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
    },
)

RELATIONS_FIELDSET = (
    "Relations",
    {"fields": ("favorites",)},
)

ADD_FIELDSET = (
    None,
    {
        "classes": ("wide",),
        "fields": (
            "email",
            "password1",
            "password2",
            "name",
            "surname",
            "phone",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ),
    },
)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    add_form = forms.AdminUserCreationForm
    form = forms.AdminUserChangeForm
    model = UserModel

    list_display = (
        "email",
        "name",
        "surname",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "name",
        "surname",
        "phone",
    )

    ordering = ("email",)

    filter_horizontal = (
        "groups",
        "user_permissions",
        "favorites",
    )

    fieldsets = (
        BASIC_FIELDSET,
        PERSONAL_INFO_FIELDSET,
        PERMISSIONS_FIELDSET,
        RELATIONS_FIELDSET,
    )

    add_fieldsets = (ADD_FIELDSET,)
