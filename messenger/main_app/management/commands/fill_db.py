from django.core.management.base import BaseCommand
from auth_app.models import MesUser
import json, os

JSON_PATH = 'messenger/management/json_files/'

def load_from_json(file_name):

    with open(os.path.join(JSON_PATH, file_name + '.json'), 
              'r', encoding='utf-8') as file:
        return json.load(file)

class Command(BaseCommand):

    def handle(self, *args, **options):

        MesUser.objects.all().delete()
        
        # brands = load_from_json('brands')
        # for brand in brands:
        #     add_brand = Brand(**brand)
        #     add_brand.save()

        user = MesUser.objects.create_user(
            username='diana', password='1234567d', first_name='Диана',
            second_name='Кретова', birth_place='Украина, Харьков',
            birth_date='1990-10-10', email=None
        )
        user.save()
        
        if input('Create superuser? (y/n) ') == 'y':
            user = MesUser.objects.create_superuser(
                username='dimag', password='1234567d', first_name='Дима',
                second_name='Гончар', birth_place='Украина, Харьков',
                birth_date='1990-10-10', email=None
            )
            user.save()
