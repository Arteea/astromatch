from config_reader import config
from httpx import AsyncClient
from urllib.parse import urlencode

from logger.logger_config import get_logger

logger = get_logger(__name__)

class GeoService:
    '''Класс для работы с GEOCODING API.'''

    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.geo_token = config.geo_token.get_secret_value()

    
    async def validate_city(self, city: str) -> tuple[str, str]:
        '''Метод для валидации отправленного пользователем города.
        С помощью запроса на API получиаем унифицированные названия городов + регион
        для последующего сохранения в БД.
        В случае если город находится в Крыму API некорректно определяет регион,поэтому вручную 
        присваеваем, если не прошла ошибка по городу
        '''
        params = {
            "address": city,
            "key": self.geo_token,
            "language": "ru",
            }
        async with AsyncClient() as client:
            response = await client.get(f"{self.base_url}?{urlencode(params)}")
            data = response.json()
        
        if response.status_code != 200 or data["status"] !="OK":
            raise ValueError("Введите корректный населенный пункт")
        
        city = region = None

        for component in data["results"][0]["address_components"]:
            if "locality" in component["types"]:
                city = component["long_name"]
            elif "administrative_area_level_1" in component["types"]:
                region = component["long_name"]
        logger.info(f"Определили город - {city} / регион - {region}")
        if not city:
            raise ValueError("Не удалось определить город. Попробуйте еще раз, либо введите вручную")
        elif not region:
            region = "Крым"
        return city, region 


    async def set_city(self, lat, lon) -> tuple[str, str]:
        '''Метод для определения города и региона по долготе и широте.
        С помощью запроса на API получиаем унифицированные названия городов + регион
        для последующего сохранения в БД.
        В случае получения координат из Крыма API некорректно определяет регион,поэтому вручную 
        присваеваем, если не прошла ошибка по городу
        '''
        params = {
            "latlng": f"{lat},{lon}",
            "key": self.geo_token,
            "language": "ru",
            }

        async with AsyncClient() as client:
            response = await client.get(f"{self.base_url}?{urlencode(params)}")
            data = response.json()

        if response.status_code != 200 or data["status"] != "OK":
            raise ValueError("Ошибка при определении местоположения")

        city = region = None

        for component in data["results"][0]["address_components"]:
            if "locality" in component["types"]:
                city = component["long_name"]
            elif "administrative_area_level_1" in component["types"]:
                region = component["long_name"]
        logger.info(f"Определили город - {city} / регион - {region}")
        if not city:
            raise ValueError("Не удалось определить город. Попробуйте еще раз, либо введите вручную")
        elif not region:
            region = "Крым"
        return city, region


geo_service = GeoService()