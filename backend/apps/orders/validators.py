from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.startswith('+'):
        raise ValidationError('Телефон должен начинаться с +')