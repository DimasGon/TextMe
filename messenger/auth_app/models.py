from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import pre_save, post_save

class MesUser(AbstractUser):

    username = models.CharField(min_length=4, max_length=20, verbose_name='Имя в системе', required=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя', required=True)
    second_name = models.CharField(max_length=20, verbose_name='Фамилия', required=True)
    email = models.EmailField(verbose_name='Эллектронный адрес')
    birth_place = models.CharField(max_length=50, verbose_name='Место рождения')
    birth_date = models.DateField(verbose_name='Дата рождения', input_format=settings.DARE_INPUT_FORMAT)
    avatar = models.ImageField(verbose_name='Аватар')
    password = models.CharField(min_length=4, max_length=20, verbose_name='Пароль', required=True)
    signin_date = models.DateTimeField(auto_now_add=True)

def before_save(sender, instance, created, **kwargs):

    print('\n\nФУНКЦИЯ before_save\nsender: {}, instance: {}\n\n'.format(sender, instance))

def after_save(sender, instance, created, **kwargs):

    print('\n\nФУНКЦИЯ after_save\nsender: {}, instance: {}\n\n'.format(sender, instance))

pre_save.connect(before_save, sender=MesUser)
post_save.connect(after_save, sender=MesUser)