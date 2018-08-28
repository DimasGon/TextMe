from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app import models

class AccountView(LoginRequiredMixin, DetailView):

    model = models.MesUser
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        search_acc = self.request.GET.get('q')

        if search_acc is not None:
            
            try:
                search_acc = models.MesUser.objects.get(username=search_acc)
            except models.MesUser.DoesNotExist:
                search_acc = None

            if search_acc:
                context['search_acc'] = search_acc  

            else:
                context['search_acc'] = 'Нет совпадений'

        return context

class SearchAccountView(LoginRequiredMixin, DetailView):

    model = models.MesUser
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'

    # def get(self, request, pk):

    #     search_acc = request.GET.get('q')

    #     if search_acc is not None:
            
    #         context = self.get_context_data()
    #         search_acc = models.MesUser.objects.get(username=search_acc)

    #         if search_acc:

    #             context['search_acc'] = search_acc

    #             return render(request, self.template_name, context)

    #         return render(request, self.template_name, context)            

    #     return super(SearchAccountView, self).get(request)
