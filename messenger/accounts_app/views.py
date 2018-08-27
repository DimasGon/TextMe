from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app import models

class AccountView(LoginRequiredMixin, DetailView):

    model = models.MesUser
    template_name = 'accounts_app/account.html'
    context_object_name = 'account'
