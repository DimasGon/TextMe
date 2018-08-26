from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, FormView
from . import models

class AccountView(DetailView):

    model = models.MesUser
    template_name = 'auth_app/account.html'
    context_object_name = 'account'

class LogInView(FormView):
    pass

class SignInView(FormView):
    pass

class LogOutView(FormView):
    pass
