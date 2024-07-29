from db.constants import (
    OTHER, MAN, WOMAN,
    USER_MINIMUM_AGE,
    PHOTO_LIMIT,
    STATE_START, 
    STATE_FINISH, 
    STATE_INTERNET_WARNING, 
    STATE_ASK_NAME,
    STATE_ASK_AGE, 
    STATE_ASK_GENDER, 
    STATE_ASK_LOOKING_FOR, 
    STATE_ASK_CITY,
    STATE_ASK_DESCRIPTION, 
    STATE_ASK_PHOTOS
)


COMMAND_START = '/sart'
COMMAND_HELP = '/help'
COMMAND_VIEW_PROFILE = '/view_profile'

INITIAL_MESSAGE = """Привіт, мене звати <b>Perfect Match</b>\n
Давай відразу перейдем на "Ти". Вважай мене своїм особистим асистентом 😉\n
Почнемо зі створення твого профілю!"""

INTERNET_WARNING_MESSAGE = """Ой, забув попередити 😔\n
Люди в інтернеті можуть видавати себе за кого завгодно і нажаль я не можу це контролювати ☹️\n
Тому, пам\'ятай про це і стався з відповідальністю"""

ASK_NAME_MESSAGE = 'Вкажи своє ім\'я, або можливо якийсь псевдонім'
ASK_AGE_MESSAGE = 'Скільки тобі років? Тільки чесно 😒'
ASK_GENDER_MESSAGE = 'Вкажи свою стать'
ASK_LOOKING_FOR_MESSAGE = 'Кого ти хочеш шукати?'
ASK_CITY_MESSAGE = 'З якого ти міста?'
ASK_DESCRIPTION_MESSAGE = 'Мені потрібен твій опис. Можеш розповісти про себе, про хобі, риси характеру.\
 Також непогано було би почути чого ти очікуєш від майбутніх знайомств'
ASK_PHOTOS_MESSAGE = f'Тепер я би хотів на тебе подивитися 😉\n\
Відправ не більше ніж {PHOTO_LIMIT} фото. Якщо стидаєшся, я не проти якихось картинок, але\
 було би непогано, якби ці картинтки хоча би якимось чином тебе охарактеризовували'
SETUP_DONE_MESSAGE = f"""Нарешті ми це зробили 😮‍💨\n
Тепер вся твоя інформація в моїй пам\'яті і її зможуть бачити інші.
Якщо хочеш глянути на свій профіль, використай цю команду {COMMAND_VIEW_PROFILE}"""

STATE_MESSAGES = {
    STATE_START: INITIAL_MESSAGE,
    STATE_INTERNET_WARNING: INTERNET_WARNING_MESSAGE,
    STATE_ASK_NAME: ASK_NAME_MESSAGE,
    STATE_ASK_AGE: ASK_AGE_MESSAGE,
    STATE_ASK_GENDER: ASK_GENDER_MESSAGE,
    STATE_ASK_LOOKING_FOR: ASK_LOOKING_FOR_MESSAGE,
    STATE_ASK_CITY: ASK_CITY_MESSAGE,
    STATE_ASK_DESCRIPTION: ASK_DESCRIPTION_MESSAGE,
    STATE_ASK_PHOTOS: ASK_PHOTOS_MESSAGE,
    STATE_FINISH: SETUP_DONE_MESSAGE
}

INITIAL_MESSAGE_RESPONSE = 'Давай 👌'
INTERNET_WARNING_RESPONSE = 'Так, розумію 👍'

UKNOWN_RESPONSE = 'Незрозуміла відповідь :('

NOT_A_NUMBER = 'Вік всього лиш цифра, але ж ЦИФРА, а не текст. Спробуй ще раз 😒'

PHOTO_IS_REQUIRED = 'Я звісно розумію, що не всі хочуть виставляти свої фото, але ж хоч якусь картинку таки знайди, будь ласка'
TOO_MANY_PHOTOS = f'Я ж напевно не просто так сказав про ліміт на фото? Але не хвилюйся, я зберіг ті які не перевищили ліміт.'
CHANGE_PHOTOS_MESSAGE = 'Всі ваші фото видалені. Тепер надішліть нові.'
PHOTOS_SAVED_MESSAGE = 'Виглядаєш неймовірно, мабуть 🙃\nЯ ж лише програма, але не сумніваюсь, що інші оцінять!'

GENDER_MESSAGE_RESPONSES = {
    MAN: 'Хлопець 👨',
    WOMAN: 'Дівчина 👩',
    OTHER: 'Не важливо'
}
WRONG_GENDER_MESSAGE = 'Я ці кнопки не просто так відправив 🤨'

TOO_YOUNG_MESSAGE = f'Вибачай, але спочатку тобі потрібно трішки підрости. Хоча би до {USER_MINIMUM_AGE}-ти'
INNAPROPRIATE_AGE_MESSAGE = f'Я звісно вражений, що ти дожив до такого віку, але мені кладно в це повірити, \
тому цього разу, давай по чесному 🙂'

ALREADY_REGISTERED_MESSAGE = 'Я досі пам\'ятаю всі твої відповіді на мої питання, можеш не хвилюватися.\
 Якщо потрібно щось змінити, для цього є відповідні команди. Рекомендую почати з /help'

TOO_LONG_NAME_MESSAGE = 'Наскільки я пам\'ятаю, найдовше ім\'я в світі має 50 символів, проте \
мені здається ми щойно знайшли нового рекордсмена 👏\n\
А якщо серйозно, то давай щось коротше'

TOO_LONG_CITY_MESSAGE = 'Вперше бачу таку довгу назву міста 👀\n\
Я сподіваюсь воно має скорочення?'

TOO_LONG_DESCRIPTION_MESSAGE = 'Вау, бачу тобі є що про себе розповісти, але це надто багато, спробуй щось коротше будь ласка 😞'
