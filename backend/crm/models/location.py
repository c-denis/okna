from django.db import models

class City(models.Model):
    """
    Модель города для адресов клиентов.
    Интегрируется с ФИАС (система нормализации адресов).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    fias_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='ФИАС ID')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Address(models.Model):
    """
    Детализированный адрес клиента.
    Связан с моделью City.
    """
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=10, verbose_name='Дом')
    building = models.CharField(max_length=10, blank=True, verbose_name='Корпус')
    apartment = models.CharField(max_length=10, blank=True, verbose_name='Квартира')
    
    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}" + \
               (f", к{self.building}" if self.building else "") + \
               (f", кв{self.apartment}" if self.apartment else "")
    
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        unique_together = ('city', 'street', 'house', 'building', 'apartment')