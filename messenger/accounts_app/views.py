from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app.models import MesUser
from . import models

class AccountView(LoginRequiredMixin, DetailView):

    model = models.AccountModel
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'

    def get_search(self, context):

        search_acc = self.request.GET.get('q')

        try:
            search_acc = models.AccountModel.objects.get(user__username=search_acc)
        except models.AccountModel.DoesNotExist:
            search_acc = None

        if search_acc and search_acc.user != self.request.user:
            context['search_acc'] = search_acc.user
        else:
            context['search_acc'] = 'Нет совпадений'

        return context

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        account = context['account']
        context['wallposts'] = account.get_wallposts()

        user_acc = models.AccountModel.objects.get(user=self.request.user)
        context['bookmarks'] = user_acc.bookmarks.all()
        context['bookmarks_amount'] = len(context['bookmarks'])

        if self.request.GET.get('q'):
            context = self.get_search(context)

        return context

    def post_wallpost(self, account_id):
        
        author = self.request.user
        account = models.AccountModel.objects.get(id=account_id)
        post_text = self.request.POST.get('wallpost')

        models.WallPostModel(author=author, account=account, post_text=post_text).save()

    def post_comment(self):
        
        author = self.request.user
        comment_text = self.request.POST.get('comment')
        to_post = int(self.request.POST.get('to_post'))
        post = models.WallPostModel.objects.get(id=to_post)

        models.CommentModel(author=author, comment_text=comment_text, to_post=post).save()

    def post_add_to_bookmarks(self, bookmark_user_id):

        bookmark = MesUser.objects.get(id=bookmark_user_id)

        user_acc = models.AccountModel.objects.get(user=self.request.user)
        user_acc.bookmarks.add(bookmark)

    def post(self, request, pk):

        if request.POST.get('wallpost'):
            self.post_wallpost(pk)

        elif request.POST.get('comment'):
            self.post_comment()

        elif request.POST.get('bookmark'):
            self.post_add_to_bookmarks(request.POST.get('bookmark'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
