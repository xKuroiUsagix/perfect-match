OTHER = 0
MAN = 1
WOMAN = 2

GENDER_CHOICES = {
    'OTHER': OTHER,
    'MAN': MAN,
    'WOMAN': WOMAN
}

USER_MINIMUM_AGE = 16
USER_MAXIMUM_AGE = 99

PHOTO_LIMIT = 5

STATE_START = 0
STATE_INTERNET_WARNING = 1
STATE_ASK_NAME = 2
STATE_ASK_AGE = 3
STATE_ASK_GENDER = 4
STATE_ASK_LOOKING_FOR = 5
STATE_ASK_CITY = 6
STATE_ASK_DESCRIPTION = 7
STATE_ASK_PHOTOS = 8
STATE_HANDLING_PHOTOS = 9
STATE_FINISH = 10

STATE_UPDATE_NAME = 11
STATE_UPDATE_CITY = 12
STATE_UPDATE_DESCRIPTION = 13
STATE_UPDATE_AGE = 14
STATE_UPDATE_PHOTOS = 15

MAX_DESCRIPTION_LENGTH = 512
MAX_CITY_LENGTH = 256
MAX_NAME_LENGTH = 64
