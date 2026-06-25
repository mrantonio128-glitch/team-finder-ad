from typing import Any

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from accounts.constants import (
    ERR_MSG_LOGIN_BANNED,
    ERR_MSG_LOGIN_INVALID_CRED,
)
from accounts.utils import clean_phone
from core.forms import GithubUrlValidationMixin

User = get_user_model()


# admin forms
class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "surname", "phone")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "surname",
            "phone",
            "avatar",
            "about",
            "github_url",
        )


class UserRegistrationForm(forms.ModelForm):
    """Frontend compliant registration form."""

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
        }

    def save(self, commit: bool = True) -> Any:
        """Hash password in this makeshift form."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Frontend compliant login form."""

    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(
        self, request: HttpRequest | None = None, *args: Any, **kwargs: Any
    ) -> None:
        """Initialize the form."""
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self) -> Any:
        """Validate the form (perform the login)."""
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise ValidationError(ERR_MSG_LOGIN_INVALID_CRED)
            if not self.user_cache.is_active:
                raise ValidationError(ERR_MSG_LOGIN_BANNED)

        return self.cleaned_data

    def get_user(self) -> Any:
        """Get cached logged-in user."""
        return self.user_cache


class ProfileEditForm(GithubUrlValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватарка",
            "about": "О себе",
            "phone": "Номер телефона",
            "github_url": "Ссылка на Github",
        }

        def clean_phone(self) -> str | None:
            """Validate and normalize phone via helper in `accounts.utils`."""
            phone: str | None = self.cleaned_data.get("phone")
            return clean_phone(phone, instance_pk=self.instance.pk)
