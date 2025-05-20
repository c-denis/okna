from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    """
    Модель ролей пользователей (оператор, координатор, менеджер, администратор).
    """
    ROLE_OPERATOR = 'operator'
    ROLE_COORDINATOR = 'coordinator'
    ROLE_MANAGER = 'manager'
    ROLE_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (ROLE_OPERATOR, 'Оператор'),
        (ROLE_COORDINATOR, 'Координатор'),
        (ROLE_MANAGER, 'Менеджер'),
        (ROLE_ADMIN, 'Администратор'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    """
    Кастомная модель пользователя на основе AbstractUser.
    Добавляет дополнительные поля, необходимые для CRM.
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Роль'
    )
    telegram_chat_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='ID чата Telegram'
    )
    
    @property
    def is_operator(self):
        return self.role and self.role.name == Role.ROLE_OPERATOR
    
    @property
    def is_manager(self):
        return self.role and self.role.name == Role.ROLE_MANAGER
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class ManagerStatus(models.Model):
    """
    Модель статусов менеджеров (мастеров) согласно ТЗ.
    """
    STATUS_FREE = 'free'
    STATUS_BUSY = 'busy'
    STATUS_DAYOFF = 'dayoff'
    STATUS_TRAINING = 'training'
    STATUS_PAIRED = 'paired'
    
    STATUS_CHOICES = [
        (STATUS_FREE, 'Свободен'),
        (STATUS_BUSY, 'На заявке'),
        (STATUS_DAYOFF, 'Выходной'),
        (STATUS_TRAINING, 'Обучение'),
        (STATUS_PAIRED, 'В паре'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='managerstatus',
        limit_choices_to={'role__name': Role.ROLE_MANAGER}
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_FREE
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user}: {self.get_status_display()}"
    
    class Meta:
        verbose_name = 'Статус менеджера'
        verbose_name_plural = 'Статусы менеджеров'