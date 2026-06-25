from typing import Any

from django.core.exceptions import ValidationError

from accounts.constants import ERR_MSG_AVATAR_SIZE, PFP_MAX_SIZE_BYTES


def validate_avatar_file_size(value: Any) -> None:
    if value.size > PFP_MAX_SIZE_BYTES:
        raise ValidationError(ERR_MSG_AVATAR_SIZE)
