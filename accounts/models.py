from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse

from accounts.constants import (
    USER_ABOUT_MAX_LEN,
    USER_NAME_MAX_LEN,
    USER_PHONE_MAX_LEN,
)
from accounts.managers import UserManager
from accounts.utils import generate_avatar
from accounts.validators import validate_avatar_file_size
from core.models import GithubLinkMixin


class User(AbstractBaseUser, PermissionsMixin, GithubLinkMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LEN)
    surname = models.CharField(max_length=USER_NAME_MAX_LEN)

    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        null=True,
        validators=[validate_avatar_file_size],
    )
    phone = models.CharField(max_length=USER_PHONE_MAX_LEN)
    about = models.TextField(
        blank=True, null=True, max_length=USER_ABOUT_MAX_LEN
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name', 'surname', 'phone')

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_absolute_url(self) -> str:
        return reverse('users:profile', kwargs={'pk': self.pk})

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add pfp."""
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
