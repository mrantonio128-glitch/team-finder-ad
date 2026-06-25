from urllib.parse import urlparse

from django.core.exceptions import ValidationError

from core.constants import ERR_GH_MSG, GH_ALLOWED_DOMAIN, GH_ALLOWED_SCHEME


def validate_github_url(value: str | None) -> str | None:
    if not value:
        return value

    parsed = urlparse(value)
    domain = parsed.netloc.lower()

    if (
        parsed.scheme not in GH_ALLOWED_SCHEME
        or domain not in GH_ALLOWED_DOMAIN
    ):
        raise ValidationError(ERR_GH_MSG)

    return value


class GithubUrlValidationMixin:
    def clean_github_url(self) -> str | None:
        return validate_github_url(
            self.cleaned_data.get('github_url'),
        )
