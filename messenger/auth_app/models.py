from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class MesUser(AbstractUser):

    first_name = models.CharField(max_length=20, verbose_name='Имя')
    second_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эллектронный адрес')
    birth_place = models.CharField(max_length=50, verbose_name='Место рождения')
    birth_date = models.DateField(verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, verbose_name='Аватар', upload_to='users_logo/')
    signin_date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
