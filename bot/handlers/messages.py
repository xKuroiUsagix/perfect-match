from db.constants import (
    OTHER, MAN, WOMAN,
    PHOTO_LIMIT,
    STATE_START, 
    STATE_FINISH, 
    STATE_INTENET_WARNING, 
    STATE_ASK_NAME,
    STATE_ASK_AGE, 
    STATE_ASK_GENDER, 
    STATE_ASK_LOOKING_FOR, 
    STATE_ASK_CITY,
    STATE_ASK_DESCRIPTION, 
    STATE_ASK_PHOTOS
)


INITIAL_MESSAGE = """<b>Вас вітає Perfect Match</b>\n
До початку вашого пошуку залишилось всього кілька кроків. Розпочнімо?"""

INTERNET_WARNING_MESSAGE = 'Будьте обережні спілкуючись в інтернеті. Іноді люди можуть видавати себе за інших,\
раджу вам сприймати все з нотками сумніву.'

ASK_NAME_MESSAGE = 'Як до вас звертатися?'
ASK_AGE_MESSAGE = 'Скільки вам років?'
ASK_GENDER_MESSAGE = 'Оберіть вашу стать'
ASK_LOOKING_FOR_MESSAGE = 'Кого ви бажаєте знайти?'
ASK_CITY_MESSAGE = 'З якого ви міста?'
ASK_DESCRIPTION_MESSAGE = 'Коротко опишіть себе. Можете розповісти про свої хобі, чого очікуєте від людини яку шукаєте і так далі.'
ASK_PHOTOS_MESSAGE = f'Надішліть не більше ніж {PHOTO_LIMIT} фото.'
SETUP_DONE_MESSAGE = 'Ваш профіль успішно створенно! Щоб переглянути його, використайте команду /view_profile'

STATE_MESSAGES = {
    STATE_START: INITIAL_MESSAGE,
    STATE_INTENET_WARNING: INTERNET_WARNING_MESSAGE,
    STATE_ASK_NAME: ASK_NAME_MESSAGE,
    STATE_ASK_AGE: ASK_AGE_MESSAGE,
    STATE_ASK_GENDER: ASK_GENDER_MESSAGE,
    STATE_ASK_LOOKING_FOR: ASK_LOOKING_FOR_MESSAGE,
    STATE_ASK_CITY: ASK_CITY_MESSAGE,
    STATE_ASK_DESCRIPTION: ASK_DESCRIPTION_MESSAGE,
    STATE_ASK_PHOTOS: ASK_PHOTOS_MESSAGE,
    STATE_FINISH: SETUP_DONE_MESSAGE
}

INITIAL_MESSAGE_RESPONSE = 'Вперед 👌'
INTERNET_WARNING_RESPONSE = 'Так, розумію 👍'

UKNOWN_RESPONSE = 'Незрозуміла відповідь :('

NOT_A_NUMBER = 'Ваша відповідь не є числом. Спробуйте ще раз.'

PHOTO_IS_REQUIRED = "Фото є обов'язковим. Якщо ви не бажаєте публікувати своє власне фото, раджу обрати картинку яка вас характеризує."
TOO_MANY_PHOTOS = f'Ви надіслали надто багато фото. Допустима кількість: {PHOTO_LIMIT}.\
\nПроте не хвилюйтесь, я зберіг ваші фото, які не перевищили ліміт.'
CHANGE_PHOTOS_MESSAGE = 'Всі ваші фото видалені. Тепер надішліть нові.'
PHOTOS_SAVED_MESSAGE = 'Ваші фото збережені :)'

GENDER_MESSAGE_RESPONSES = {
    MAN: 'Хлопець 👨',
    WOMAN: 'Дівчина 👩',
    OTHER: 'Не важливо'
}
WRONG_GENDER_MESSAGE = 'Будь ласка, Оберіть стать використовуючи одну з кнопок.'

INNAPROPRIATE_AGE = 'too young'

ALREADY_REGISTERED_MESSAGE = 'Ви вже створили свій профіль. Якщо ви бажаєте щось змінити, використайте одну з відповідних команд.'