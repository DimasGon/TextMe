from django.db import models
from django.db.models.signals import post_save
from auth_app.models import MesUser

class ThreadModel(models.Model):

    participants = models.ManyToManyField(MesUser)
    last_message_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    last_message_text = models.TextField()

    def get_partner(self, user):

        for obj in self.participants.all():
            if obj != user:
                return obj

class MessageModel(models.Model):

    text = models.TextField(verbose_name='Текст сообщения')
    sender = models.ForeignKey(MesUser, on_delete=models.DO_NOTHING)
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

def update_last_thread(sender, instance, created, **kwargs):

    if not created:
        return
    
    thread = ThreadModel.objects.get(id=instance.thread.id)
    thread.last_message_time = instance.time
    thread.last_message_text = instance.text
    thread.save()

post_save.connect(update_last_thread, MessageModel)