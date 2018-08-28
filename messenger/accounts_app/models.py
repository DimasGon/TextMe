from django.db import models
from auth_app.models import MesUser

class WallPostModel(models.Model):
    pass

class CommentModel(models.Model):
    pass

class AccountModel(models.Model):

    user = models.ForeignKey(MesUser, on_delete=models.CASCADE)
    # wallpost = models.ForeignKey(WallPostModel, on_delete=models.DO_NOTHING)
