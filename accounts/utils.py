import secrets
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from accounts.constants import (
    PFP_DEFAULT_FONT_PATH,
    PFP_DEFAULT_SHAPE,
    PFP_DEFAULT_TEXT_COLOR,
    PFP_DEFAULT_TEXT_OFFSET,
)


def generate_avatar(name: str) -> ContentFile:
    letter = name[0].upper() if name else '?'
    size = PFP_DEFAULT_SHAPE

    bg_color = tuple(secrets.choice(range(100, 201)) for _ in range(3))

    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)

    font_size = int(min(PFP_DEFAULT_SHAPE) * 0.5)
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
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{letter}.png')
