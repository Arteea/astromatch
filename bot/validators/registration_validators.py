import re
from typing import Union
from utils.zodiac_buttons import list_of_zodiac
phone_regex = r'^\+7\d{10}$'


class RegistrationValidator:

    @staticmethod
    def validate_phone(phone: str, phone_regex=r'^\+7\d{10}$'):
        if not isinstance(phone, str):
            raise TypeError("Номер телефона должен быть передан в видуе строки")
        if phone.startswith("7") and len(phone) == 11:
            ###Добавляем "+" т.к. телеграм при первом неудачном сценарии и повторной отправке номера некорректно достает контакт,без символа
            phone = "+" + phone
        if not re.fullmatch(phone_regex, phone):
            raise ValueError(f'❌Скиньте контакт в формате номера РФ')
        return phone

    @staticmethod
    def validate_username(username: str) -> str:

        if not isinstance(username, str):
            raise TypeError("Никнейм должен быть строкой")
        if not (2 < len(username) <= 40):
            raise ValueError("❌Никнейм должен быть от 3 до 40 символов")
        if re.search(r"[<>{}\[\]]", username):
            raise ValueError("❌Недопустимые символы в никнейме")
        return username.strip()
    
    @staticmethod
    def validate_gender(gender: str) -> str:
        if not isinstance(gender, str):
            raise TypeError("Пол должен быть в виде строки")
        if not gender in ("male","female"):
            raise ValueError("❌Выберите корректный пол нажав на кнопку")
        return gender
    
    @staticmethod
    def validate_age(age:str) -> int:
        try:
            age_int = int(age) 
            if age_int < 16 or age_int > 100:
                raise ValueError("❌Введите корректный возраст от 16")
            return age_int 
        except ValueError:
            raise ValueError("❌Введите корректный возраст в виде числа")
        
    @staticmethod
    def validate_description(description:str) -> str:
        if len(description) > 500:
            raise ValueError('Подкорректируйте описание.Лимит -500 символов')
        return description
    
    @staticmethod
    def validate_zodiac(zodiac:str) -> str:
        if zodiac not in list_of_zodiac:
            raise ValueError("❌Выберите корректный знак зодиака, попробуйте еще раз")
        return zodiac