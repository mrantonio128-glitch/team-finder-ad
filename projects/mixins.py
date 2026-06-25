"""Project mixins."""

from typing import Any

from django.contrib.auth.mixins import AccessMixin


class IsOwnerMixin(AccessMixin):
    """Mixin for checking whether user is an owner of the project."""

    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """Only project owner may do the thing."""
        project = self.get_object()
        if request.user != project.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
