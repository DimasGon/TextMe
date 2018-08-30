from django.db import models
from auth_app.models import MesUser

class AccountModel(models.Model):

    user = models.ForeignKey(MesUser, on_delete=models.CASCADE, related_name='Пользователь')
    bookmarks = models.ManyToManyField(MesUser, related_name='Закладки')

    def get_wallposts(self):

        wallposts = self.wallpostmodel_set.model.objects.filter(
            account=self.id).order_by('-created')
        
        for post in wallposts:
            comments = post.get_comments()
            post.comments = comments
        
        return wallposts

    def __str__(self):
        return self.user.username

class WallPostModel(models.Model):
    
    author = models.ForeignKey(MesUser, on_delete=models.DO_NOTHING)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    post_text = models.TextField(verbose_name='Текст поста')
    created = models.DateTimeField(auto_now_add=True)

    def get_comments(self):

        comments = self.commentmodel_set.model.objects.filter(
            to_post=self.id).order_by('-created').reverse()
        
        return comments

    def __str__(self):
        return 'Автор: ' + self.author.username

class CommentModel(models.Model):

    author = models.ForeignKey(MesUser, on_delete=models.DO_NOTHING)
    comment_text = models.TextField(verbose_name='Текст комментария')
    to_post = models.ForeignKey(WallPostModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'К посту ' + self.to_post.account.user.username
