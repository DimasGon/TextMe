from django.db import models
from auth_app.models import MesUser

class AccountModel(models.Model):

    user = models.ForeignKey(MesUser, on_delete=models.CASCADE)

    def get_wallposts(self):

        print('\n\n', self.wallpostmodel_set.model.objects.all(), '\n\n')
        
        return self.wallpostmodel_set.model.objects.all()

class WallPostModel(models.Model):
    
    author = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    post_text = models.TextField(verbose_name='Текст поста')
