from django.core.management.base import BaseCommand
from crm.services.fias_integration import FIASIntegration
from crm.models import City

class Command(BaseCommand):
    help = 'Импорт городов из ФИАС в базу данных'

    def handle(self, *args, **options):
        self.stdout.write('Начало импорта городов из ФИАС...')
        
        try:
            # Получаем данные из ФИАС
            cities_data = FIASIntegration.get_all_cities()
            
            # Импортируем города
            for city_data in cities_data:
                City.objects.update_or_create(
                    fias_id=city_data['fias_id'],
                    defaults={
                        'name': city_data['name'],
                        'region': city_data.get('region', '')
                    }
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Успешно импортировано {len(cities_data)} городов')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка импорта: {str(e)}')
            )