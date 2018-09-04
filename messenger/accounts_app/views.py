from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from auth_app.models import MesUser
from . import models

class RusJsonResponse(JsonResponse):

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=False, *args, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, *args, **kwargs)

class JSONAccountView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):

        adress = request.META.get('HTTP_REFERER')
        id = int(adress[adress.find('account/') + 8])

        account = models.AccountModel.objects.get(id=id)
        wallposts = account.get_wallposts()
        user_acc = models.AccountModel.objects.get(user=request.user)
        bookmarks = user_acc.bookmarks.all()
        # bookmarks_amount = len(bookmarks)

        html_page = render_to_string(
            'accounts_app/json_account.html',
            {'account': account, 'wallposts': wallposts, 'bookmarks': bookmarks},
            request
        )

        return RusJsonResponse({'html_page': html_page})

class AccountRedirectView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):
        return HttpResponseRedirect('/account/{}'. format(request.user.id))

class AccountView(LoginRequiredMixin, DetailView):

    model = models.AccountModel
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'
    login_url = '/login'

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

        print('\n\nДобавил')

    def post(self, request, pk):

        if request.POST.get('wallpost'):
            
            self.post_wallpost(pk)

            account = models.AccountModel.objects.get(id=pk)
            wallposts = account.get_wallposts()
            
            wall = render_to_string(
                'accounts_app/includes/json_wallposts.html',
                {'wallposts': wallposts, 'account': account},
                request
            )

            return RusJsonResponse({'wall': wall})

        elif request.POST.get('comment'):
            self.post_comment()
            return RusJsonResponse(None)

        elif request.POST.get('bookmark'):
            self.post_add_to_bookmarks(request.POST.get('bookmark'))
            return RusJsonResponse(None)

        print('\n\n{}\n\n'.format(request.POST))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AccountSettingsView(LoginRequiredMixin, UpdateView):
    
    login_url = '/login'
    success_url = '/account'
    model = MesUser
    fields = ('first_name', 'second_name', 'email', 'birth_place', 'birth_date', 'avatar')
    template_name = 'accounts_app/form.html'
