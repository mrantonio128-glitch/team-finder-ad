from typing import Any

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    PasswordChangeView as AuthPasswordChangeView,
)
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.constants import FilterType, USER_PAGINATE_BY
from accounts.forms import (
    ProfileEditForm,
    UserLoginForm,
    UserRegistrationForm,
)
from accounts.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class SignInView(AuthLoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('projects:list')


class LogoutView(View):
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        logout(request)
        return redirect('projects:list')


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = USER_PAGINATE_BY

    FILTER_QUERIES = {
        FilterType.OWNERS_OF_FAVORITES:
            'owned_projects__interested_users',
        FilterType.OWNERS_OF_PARTICIPATING:
            'owned_projects__participants',
        FilterType.INTERESTED: 'favorites__owner',
        FilterType.PARTICIPANTS: 'participated_projects__owner',
    }

    def get_queryset(self) -> QuerySet:
        """Return sorted, optionally filtered users."""
        qs = User.objects.all().order_by('-id')
        filter_type = self.request.GET.get('filter')
        user = self.request.user

        if filter_type and user.is_authenticated:
            lookup = self.FILTER_QUERIES.get(filter_type)
            if lookup:
                qs = qs.filter(**{lookup: user})

        return qs.distinct()

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter', '')
        return context


class UserDetailView(DetailView):
    """User profile."""

    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(
        self, queryset: QuerySet | None = None
    ) -> User | AnonymousUser:
        """Edit current user."""
        return self.request.user

    def get_success_url(self) -> Any:

        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    """Password change view."""

    template_name = 'users/change_password.html'

    def get_success_url(self) -> Any:
        """Redirect to profile view."""
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})
