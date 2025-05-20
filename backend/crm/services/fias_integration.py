import requests
from django.conf import settings
from django.core.cache import cache
from ..models import City

class FIASIntegration:
    """
    Интеграция с ФИАС (Федеральная информационная адресная система).
    Обеспечивает автоподстановку и нормализацию адресов.
    """
    
    BASE_URL = 'https://fias.nalog.ru/API'
    
    @classmethod
    def search_city(cls, query):
        """
        Поиск города по названию.
        
        Args:
            query (str): Название города или части
            
        Returns:
            list: Список найденных городов
        """
        cache_key = f'fias_city_search_{query}'
        cached = cache.get(cache_key)
        if cached:
            return cached
            
        try:
            response = requests.get(
                f'{cls.BASE_URL}/search',
                params={'query': query, 'type': 'city'},
                timeout=3
            )
            data = response.json()
            
            # Кэшируем на 1 час
            cache.set(cache_key, data, 3600)
            return data
        except requests.RequestException:
            # Возвращаем города из базы, если API недоступно
            return list(City.objects.filter(name__icontains=query).values('id', 'name'))
    
    @classmethod
    def get_address_suggestions(cls, city_id, query):
        """
        Получение подсказок по адресу.
        
        Args:
            city_id (int): ID города в ФИАС
            query (str): Часть адреса (улица, дом)
            
        Returns:
            list: Варианты адресов
        """
        cache_key = f'fias_address_{city_id}_{query}'
        cached = cache.get(cache_key)
        if cached:
            return cached
            
        try:
            response = requests.get(
                f'{cls.BASE_URL}/suggest',
                params={'city_id': city_id, 'query': query},
                timeout=3
            )
            data = response.json()
            cache.set(cache_key, data, 3600)
            return data
        except requests.RequestException:
            return []
    
    @classmethod
    def update_city_fias_data(cls):
        """
        Обновление данных городов из ФИАС.
        Запускается периодически (например, через cron).
        """
        try:
            response = requests.get(f'{cls.BASE_URL}/cities', timeout=10)
            cities = response.json()
            
            for city_data in cities:
                City.objects.update_or_create(
                    fias_id=city_data['fias_id'],
                    defaults={'name': city_data['name']}
                )
            
            return True
        except requests.RequestException as e:
            print(f"Ошибка обновления городов из ФИАС: {e}")
            return False