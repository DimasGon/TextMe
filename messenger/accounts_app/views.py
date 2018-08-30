from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

class AccountView(LoginRequiredMixin, DetailView):

    model = models.AccountModel
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'

    def search(self, context):

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

        if self.request.GET.get('q'):
            context = self.search(context)

        return context

    def post(self, request):

        # if request.POST.get('wallpost')

        return super().post(request)
