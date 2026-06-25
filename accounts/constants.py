from enum import StrEnum

from django.conf import settings

# model User
USER_NAME_MAX_LEN = 124
USER_PHONE_MAX_LEN = 12
USER_ABOUT_MAX_LEN = 256

USER_PAGINATE_BY = 12


class FilterType(StrEnum):
    OWNERS_OF_FAVORITES = 'owners-of-favorite-projects'
    OWNERS_OF_PARTICIPATING = 'owners-of-participating-projects'
    INTERESTED = 'interested-in-my-projects'
    PARTICIPANTS = 'participants-of-my-projects'


# utils pfp gen
PFP_MAX_SIZE_MB = 2
PFP_MAX_SIZE_BYTES = PFP_MAX_SIZE_MB * 1024 * 1024
PFP_DEFAULT_SHAPE: tuple[int, int] = (200, 200)
PFP_DEFAULT_TEXT_OFFSET: tuple[int, int] = (0, -20)
PFP_DEFAULT_TEXT_COLOR = (255, 255, 255)
PFP_DEFAULT_FONT_PATH = (
    settings.BASE_DIR
    / 'static'
    / 'fonts'
    / 'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf'
)

# err
ERR_MSG_LOGIN_INVALID_CRED = 'Неверный имейл или пароль'
ERR_MSG_LOGIN_BANNED = 'Этот аккаунт заблокирован'
ERR_MSG_PHONE_EXISTS = (
    'Этот номер телефона уже используется другим пользователем.'
)
ERR_MSG_PHONE_FORMAT = (
    'Номер телефона должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX'
)
ERR_MSG_AVATAR_SIZE = (
    f'Размер файла аватара не должен превышать {PFP_MAX_SIZE_MB} МБ.'
)
