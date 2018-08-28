from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app import models

class AccountView(LoginRequiredMixin, DetailView):

    model = models.MesUser
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'

    def search(self, context):
        
        search_acc = self.request.GET.get('q')
            
        try:
            search_acc = models.MesUser.objects.get(username=search_acc)
        except models.MesUser.DoesNotExist:
            search_acc = None

        if search_acc and search_acc != self.request.user:
            context['search_acc'] = search_acc
        else:
            context['search_acc'] = 'Нет совпадений'

        return context

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.GET.get('q'):
            context = self.search(context)

        return context
