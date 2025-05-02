from config_reader import config
from httpx import AsyncClient
from urllib.parse import urlencode

from logger.logger_config import get_logger

logger = get_logger(__name__)

class GeoService:
    '''Класс для работы с GEOCODING API для определения города и региона(области) по долготе и широте,либо по названию города'''

    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.geo_token = config.geo_token.get_secret_value()

    
    async def validate_city(self, city):
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

        if not city:
            raise ValueError("Не удалось определить город. Попробуйте еще раз, либо введите вручную")
        elif not region:
            region = "Крым"
        return city, region 


    async def set_city(self, lat, lon) -> tuple[str, str]:
        
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

        if not city:
            raise ValueError("Не удалось определить город. Попробуйте еще раз, либо введите вручную")
        elif not region:
            region = "Крым"
        return city, region


geo_service = GeoService()