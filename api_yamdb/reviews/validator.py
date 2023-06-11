from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_years(value):
    """Проверка года издания произведения"""
    if value > timezone.now().year:
        raise ValidationError("Год указан неверно!",
                              params={'value': value},)
