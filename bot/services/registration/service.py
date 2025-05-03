from validators.registration_validators import RegistrationValidator as validator
from geoapi.geoservice import geo_service
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from typing import Optional, Tuple


from logger.logger_config import get_logger

logger = get_logger(__name__)

class RegistrationService:
    '''Сервисный класс, отвечающий за вспомогательные функции, используемые при регистрации пользователя.
       Используется в процессе регистрации для обработки поступающих от пользователя
       данных,медиафайлов, форматирования информации анкеты.
       Атрибуты:
            user_id (int): Уникальный идентификатор пользователя
    '''

    def __init__(self, user_id: int):
        self.user_id = user_id
    
    #Методы-обертки над валидатором,в дальнейшем будем гулять в бд 
    def set_phone(self, phone):
        return validator.validate_phone(phone)

    def set_username(self, name):
        return validator.validate_username(name)
    
    def set_gender(self, gender):
        return validator.validate_gender(gender)
    
    def set_age(self, age: str) -> int:
        return validator.validate_age(age)
    
    def set_description(self, description: str) -> str:
        return validator.validate_description(description)
    
    def set_zodiac(self, zodiac: str) -> str:
        return validator.validate_zodiac(zodiac)

    async def set_city(self, lat=None, lon=None, city=None):
        """
        Определяет город по координатам или названию.
        Args:
            lat (float, optional): Широта
            lon (float, optional): Долгота
            city (str, optional): Название города
        Returns:
            Tuple[str, str]: Название города и региона согласно сервисам Google
        """
        if not city:
            city, region = await geo_service.set_city(lat, lon)
        elif not lat or not lon:
            city, region = await geo_service.validate_city(city)
        return city, region
    
    async def get_media_id_from_message(self, message: Message) -> str:
        '''В данном методе:
            -определяем тип медиа
            -в случае с фото достаем file_id лучшего разрешения фото [-1]
            Args:
                message (Message): Объект Message, откуда будем извлекать file_id
            Returns:
                file_id (str): Идентификатор медиафайла телеграмм с добавленным
                к file_id префиксом  типа файла для удобства дальнешего 
                использования. Пример: "media:"/"photo:" + file_id 
            '''
        if message.photo:
            file_id = message.photo[-1].file_id
            file_id = "photo:" + file_id
        elif message.video:
            file_id = message.video.file_id
            file_id = "video:" + file_id
        return file_id
    
    async def collect_media_in_mediagroup(self, media: list[str]) -> MediaGroupBuilder:
        '''
        Формирует MediaGroup из списка file_id медиафайлов.

        Args:
            media (list[str]): Список media_id c префиксами ("photo:", "video:")

        Returns:
            MediaGroupBuilder: собранная группа медиафайлов
        '''
        media_group = MediaGroupBuilder()
        for mediafile in media:
            if mediafile.startswith("photo:"):
                media_group.add_photo(media=mediafile.lstrip("photo:"))
            elif mediafile.startswith("video:"):
                media_group.add_video(media=mediafile.lstrip("video:"))
        return media_group
    
    @staticmethod
    def format_user_info(user_data: dict) -> str:
        '''
        Извлекает из словаря общую информацию от пользователя
        и форматирует для отображения в виде анкеты.
        
        Args:
            user_data (dict): Словарь данных пользователя введенных при 
            регистрации и полученных из Redis Hash.
        Returns:
            str: Форматированная анкета в виде строки
        '''
        username = user_data.get("username", "Не указано")
        gender = user_data.get("gender", "Не указано").capitalize()
        age = user_data.get("age", "Не указано")
        zodiac = user_data.get("zodiac_sign", "Не указано").capitalize()
        description = user_data.get("description", "Без описания")
        return f"👤 {username}\n🔹 Пол: {gender}\n🔹 Возраст: {age}\n🔹 Знак зодиака: {zodiac}\n📝 {description}"