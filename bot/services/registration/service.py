from validators.registration_validators import RegistrationValidator as validator
from geoapi.geoservice import geo_service
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from aiogram.utils.media_group import MediaGroupBuilder
from typing import Optional, Tuple


from logger.logger_config import get_logger

logger = get_logger(__name__)

class RegistrationService:

    def __init__(self, user_id: int):
        self.user_id = user_id
    
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
        if not city:
            city, region = await geo_service.set_city(lat, lon)
        elif not lat or not lon:
            city, region = await geo_service.validate_city(city)
        return city, region
    
    async def get_media_id_from_message(self, message: Message) -> str:
        '''В данном методе:
            -определяем тип медиа
            -в случае с фото достаем file_id лучшего разрешения фото [-1]
            -добавляем префикс к file_id с типом файла для удобства сборки и 
            отображения медиафайлов профиля, а также дальнейшего сохранения в бд'''

        if message.photo:
            file_id = message.photo[-1].file_id
            file_id = "photo:" + file_id
        elif message.video:
            file_id = message.video.file_id
            file_id = "video:" + file_id
        return file_id
    
    async def collect_media_in_mediagroup(self, media):
        media_group = MediaGroupBuilder()
        for mediafile in media:
            logger.info(f"mediafile --- {mediafile}")
            if mediafile.startswith("photo:"):
                media_group.add_photo(media=mediafile.lstrip("photo:"))
            elif mediafile.startswith("video:"):
                media_group.add_video(media=mediafile.lstrip("video:"))
        return media_group
    
    @staticmethod
    def format_user_info(user_data: dict) -> str:
        username = user_data.get("username", "Не указано")
        gender = user_data.get("gender", "Не указано").capitalize()
        age = user_data.get("age", "Не указано")
        zodiac = user_data.get("zodiac_sign", "Не указано").capitalize()
        description = user_data.get("description", "Без описания")

        return f"👤 {username}\n🔹 Пол: {gender}\n🔹 Возраст: {age}\n🔹 Знак зодиака: {zodiac}\n📝 {description}"