from typing import Optional

from db.constants import MAN, WOMAN, OTHER

from .messages import GENDER_MESSAGE_RESPONSES


def get_gender(text_decription: str) -> Optional[int]:
    if text_decription == GENDER_MESSAGE_RESPONSES[MAN]:
        return MAN
    if text_decription == GENDER_MESSAGE_RESPONSES[WOMAN]:
        return WOMAN
    if text_decription == GENDER_MESSAGE_RESPONSES[WOMAN]:
        return OTHER
