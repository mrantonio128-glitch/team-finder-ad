import re
import secrets
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from accounts.constants import (
    PFP_DEFAULT_FONT_PATH,
    PFP_DEFAULT_SHAPE,
    PFP_DEFAULT_TEXT_COLOR,
    PFP_DEFAULT_TEXT_OFFSET,
    ERR_MSG_PHONE_FORMAT,
    ERR_MSG_PHONE_EXISTS,
)

BG_COLOR_MIN = 100
BG_COLOR_MAX = 200
BG_COLOR_CHANNELS = 3
FONT_SCALE = 0.5


def generate_avatar(name: str) -> ContentFile:
    letter = name[0].upper() if name else "?"
    size = PFP_DEFAULT_SHAPE

    bg_color = tuple(
        secrets.choice(range(BG_COLOR_MIN, BG_COLOR_MAX + 1))
        for _ in range(BG_COLOR_CHANNELS)
    )

    image = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(image)

    font_size = int(min(PFP_DEFAULT_SHAPE) * FONT_SCALE)
    try:
        font = ImageFont.truetype(PFP_DEFAULT_FONT_PATH, font_size)
    except OSError:
        font = ImageFont.load_default(size=font_size)

    left, top, right, bottom = draw.textbbox((0, 0), letter, font=font)
    text_w = right - left
    text_h = bottom - top

    x = (size[0] - text_w) / 2 + PFP_DEFAULT_TEXT_OFFSET[0]
    y = (size[1] - text_h) / 2 + PFP_DEFAULT_TEXT_OFFSET[1]

    draw.text((x, y), letter, fill=PFP_DEFAULT_TEXT_COLOR, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")


def clean_phone(phone: str | None, instance_pk: int | None = None) -> str | None:
    """Validate and normalize phone field used in forms."""
    if phone is None:
        return phone

    if phone.startswith("8") and len(phone) == 11:
        phone = "+7" + phone[1:]

    if not re.match(r"^\+7\d{10}$", phone):
        raise ValidationError(ERR_MSG_PHONE_FORMAT)

    User = get_user_model()
    if User.objects.filter(phone=phone).exclude(pk=instance_pk).exists():
        raise ValidationError(ERR_MSG_PHONE_EXISTS)

    return phone
