from django.contrib.auth.models import BaseUserManager

class AccountManager(BaseUserManager):
    """Кастомный менеджер для модели Account"""
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields['is_superuser'] = True # может заходить в админку
        extra_fields['is_staff'] = True # может делать все то что хочет в админ что разрешено
        extra_fields['is_active'] = True # не заблокирован
        return self.create_user(username, password, **extra_fields)