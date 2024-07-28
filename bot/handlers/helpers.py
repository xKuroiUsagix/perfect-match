from db.constants import MAN, WOMAN, OTHER

from .messages import GENDER_MESSAGE_RESPONSES


def get_gender(text_decription: str) -> int:
    if text_decription == GENDER_MESSAGE_RESPONSES[MAN]:
        return MAN
    if text_decription == GENDER_MESSAGE_RESPONSES[WOMAN]:
        return WOMAN
    return OTHER
