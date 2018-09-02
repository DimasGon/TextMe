from django.contrib import admin
from . import models

admin.site.register(models.ThreadModel)
admin.site.register(models.MessageModel)
