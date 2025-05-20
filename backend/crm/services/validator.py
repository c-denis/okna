import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PhoneValidator:
    """
    Валидатор телефонных номеров.
    Поддерживает российские номера в различных форматах.
    """
    
    PHONE_REGEX = re.compile(r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$')
    
    def __call__(self, value):
        if not self.PHONE_REGEX.match(value):
            raise ValidationError(
                _('Введите корректный номер телефона. Пример: +79991234567 или 89991234567')
            )
        
        # Нормализация номера
        normalized = re.sub(r'[^\d]', '', value)
        if normalized.startswith('8'):
            normalized = '7' + normalized[1:]
        elif not normalized.startswith('7'):
            normalized = '7' + normalized
        
        return f'+{normalized}'

class AddressValidator:
    """
    Валидатор адресов.
    Проверяет обязательные поля и формат данных.
    """
    
    def validate_address(self, address_data):
        """
        Проверка данных адреса.
        
        Args:
            address_data (dict): {
                'city': str,
                'street': str,
                'house': str,
                'building': str (optional),
                'apartment': str (optional)
            }
            
        Raises:
            ValidationError: Если данные невалидны
        """
        errors = {}
        
        if not address_data.get('city'):
            errors['city'] = _('Укажите город')
        
        if not address_data.get('street'):
            errors['street'] = _('Укажите улицу')
        
        if not address_data.get('house'):
            errors['house'] = _('Укажите номер дома')
        
        if errors:
            raise ValidationError(errors)
        
        return True