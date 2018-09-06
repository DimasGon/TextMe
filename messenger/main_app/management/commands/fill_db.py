from django.core.management.base import BaseCommand
from auth_app.models import MesUser
from accounts_app.models import AccountModel
import json, os

JSON_PATH = 'messenger/management/json_files/'

def load_from_json(file_name):

    with open(os.path.join(JSON_PATH, file_name + '.json'), 
              'r', encoding='utf-8') as file:
        return json.load(file)

class Command(BaseCommand):

    def handle(self, *args, **options):

        MesUser.objects.all().delete()
        AccountModel.objects.all().delete()
        
        # brands = load_from_json('brands')
        # for brand in brands:
        #     add_brand = Brand(**brand)
        #     add_brand.save()

        user = MesUser.objects.create_user(
            username='diana', password='1234567d', first_name='Диана',
            second_name='Кретова', birth_place='Украина, Харьков',
            birth_date='2000-6-7', email=None
        )
        user.save()
        
        AccountModel(user=user).save()

        user = MesUser.objects.create_user(
            username='c1kzy', password='1234567d', first_name='Лонг',
            second_name='Нгуен', birth_place='Украина, Харьков',
            birth_date='1999-11-24', email=None
        )
        user.save()
        
        AccountModel(user=user).save()

        user = MesUser.objects.create_user(
            username='slidex', password='1234567d', first_name='Никита',
            second_name='Киях', birth_place='Украина, Харьков',
            birth_date='1999-8-11', email=None
        )
        user.save()
        
        AccountModel(user=user).save()

        user = MesUser.objects.create_user(
            username='mops', password='1234567d', first_name='Руслан',
            second_name='Панченко', birth_place='Украина, Харьков',
            birth_date='1999-1-17', email=None
        )
        user.save()
        
        AccountModel(user=user).save()
        
        if input('Create superuser? (y/n) ') == 'y':
            user = MesUser.objects.create_superuser(
                username='dimag', password='1234567d', first_name='Дима',
                second_name='Гончар', birth_place='Украина, Харьков',
                birth_date='1998-9-3', email=None
            )
            user.save()

            AccountModel(user=user).save()
