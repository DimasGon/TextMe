from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from . import models
from . import forms
from main_app import mixins

class AccountView(LoginRequiredMixin, DetailView):

    model = models.MesUser
    template_name = 'auth_app/account.html'
    context_object_name = 'account'

class LogInView(mixins.AnonRequired, FormView):
    
    form_class = forms.LogInForm
    template_name = 'auth_app/form.html'
    success_url = '/account/'
    context_object_name = 'form'

    def post(self, request):
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            login(request, user)

            return redirect(self.success_url + str(request.user.id))

        form = self.form_class(request.POST)

        return render(request, 'auth_app/form.html', {'form': form})

    def get_context_data(self, *args, **kwargs):

        context = super(LogInView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Вход'

        return context

class SignInView(mixins.AnonRequired, FormView):
    
    form_class = forms.SignInForm
    template_name = 'auth_app/form.html'
    success_url = '/account/'

    def post(self, request):

        print('\n\n{}\n\n'.format(request.FILES))

        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect(self.success_url + str(user.id))
        
        return render(request, 'auth_app/form.html', {'form': form})
    
    def get_context_data(self, *args, **kwargs):

        context = super(SignInView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Регистрация'

        return context

class LogOutView(LoginRequiredMixin, TemplateView):
    
    template_name = 'auth_app/form.html'
    success_url = '/'

    def get_context_data(self, *args, **kwargs):

        context = super(LogOutView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Выход'

        return context

    def post(self, request):

        logout(request)

        return redirect(self.success_url)
