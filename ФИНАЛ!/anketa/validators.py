from typing import Optional


GENDER_MAP = {
    1: 'мужской',
    2: 'женский',
    3: 'не знаю',
}
'''
def validate_group(text: str) -> Optional[int]:
        group = int(text)
        return group
'''
def validate_gender(text: str) -> Optional[int]:
    try:
        gender = int(text)
    except (TypeError, ValueError):
        return None

    if gender in GENDER_MAP:
        return gender


def gender_hru(gender: int) -> Optional[str]:
    return GENDER_MAP.get(gender)


def validate_age(text: str) -> Optional[int]:
    try:
        age = int(text)
    except (TypeError, ValueError):
        return None

    if age < 0 or age > 100:
        return None
    return age

def validate_phone(text: str) -> Optional[int]:

    try:
        phone = int(text)
    except (TypeError, ValueError):
        return None
    phone = str(phone)
    if len(phone)!= 11:
        return None
    return phone


def validate_mail(text: str) -> Optional[int]:
    mail = str(text)
    if '@' not in mail:
        return None
    return mail