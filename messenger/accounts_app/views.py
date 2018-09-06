from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from auth_app.models import MesUser
from main_app.serializers import RusJsonResponse
from . import models

# -------------------- API -------------------- #
class JSONAccountView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):

        adress = request.META.get('HTTP_REFERER')
        id = int(adress[adress.find('account/') + 8])

        account = models.AccountModel.objects.get(id=id)
        wallposts = account.get_wallposts()
        user_acc = models.AccountModel.objects.get(user=request.user)
        bookmarks = user_acc.bookmarks.all()

        html_page = render_to_string(
            'accounts_app/json_account.html',
            {'account': account, 'wallposts': wallposts, 'bookmarks': bookmarks},
            request
        )

        return RusJsonResponse({'html_page': html_page})

class JSONBookamrksView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):

        user_acc = models.AccountModel.objects.get(user=request.user)
        bookmarks = user_acc.bookmarks.all()
        bookmarks_amount = len(bookmarks)

        html_page = render_to_string(
            'accounts_app/json_bookmarks.html',
            {'user_id': user_acc.user.id, 'bookmarks': bookmarks, 'bookmarks_amount': bookmarks_amount},
            request
        )

        return RusJsonResponse({'html_page': html_page})

# -------------------- КОНТРОЛЛЕРЫ -------------------- #
class AccountRedirectView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):
        return HttpResponseRedirect('/account/{}'. format(request.user.id))

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts_app/account.html'

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

        if request.POST.get('wallpost') or request.POST.get('comment'):

            if request.POST.get('wallpost'):
                self.post_wallpost(pk)
            else:
                self.post_comment()

            return redirect('/account/api')

        elif request.POST.get('bookmark'):

            self.post_add_to_bookmarks(pk)

            return redirect('/account/api/bookmarks')

        elif request.POST.get('search'):
            
            search_acc = request.POST.get('search')
            error = False

            try:
                search_acc = models.AccountModel.objects.get(user__username=search_acc)
                if search_acc and search_acc.user != request.user:
                    search_acc = search_acc.user
                else:
                    error = 'Себя нельзя добавить в закладки'

            except models.AccountModel.DoesNotExist:
                error = 'Нет совпадений'

            html_page = render_to_string(
                'accounts_app/json_bookmarks.html',
                {'user_id': request.user.id, 'error': error, 'search_acc': search_acc},
                request
            )

            return RusJsonResponse({'html_page': html_page})

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AccountSettingsView(LoginRequiredMixin, UpdateView):
    
    login_url = '/login'
    success_url = '/account'
    model = MesUser
    fields = ('first_name', 'second_name', 'email', 'birth_place', 'birth_date', 'avatar')
    template_name = 'accounts_app/form.html'
