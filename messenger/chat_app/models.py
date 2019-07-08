from django.db import models
from django.db.models.signals import post_save
from auth_app.models import MesUser

class MongoServerModel(models.Model):

    is_started = models.BooleanField(verbose_name='Статус работы MongoDB', default=False)
    process_id = models.IntegerField(verbose_name='PID процесса, в котором работает MongoDB', default=-1)
    updated_at = models.DateTimeField(verbose_name='Дата и время обновления статуса MongoDB', auto_now_add=True)

    def __str__(self):
        return 'Сервер MongoDB'

    @staticmethod
    def get_model():
        return MongoServerModel.objects.get(id=1)


class ChatModel(models.Model):
    
    participants = models.ManyToManyField(MesUser)
    mongo_collection = models.CharField(max_length=100, primary_key=True)
    last_message_text = models.TextField(blank=True, null=True)
    last_message_time = models.CharField(max_length=30)

    def __str__(self):
        return self.mongo_collection

    def get_partner(self, user):
        return self.participants.all().exclude(id=user.id)[0]
