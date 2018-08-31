from django.shortcuts import render, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, View
from auth_app.models import MesUser
from . import models

class EmptyChatView(TemplateView):
    template_name = 'chat_app/chat.html'

class StartChatView(View):

    def get(self, request, partner_id):

        try:
            partner = MesUser.objects.get(id=partner_id)

        except MesUser.DoesNotExist:
            raise Http404('Пользователя не существует')

        return render(request, 'chat_app/chat.html', {
            'partner': partner,
            'show': 'start',
        })

    def post(self, request, partner_id):
        
        mes_text = request.POST.get('mes_text')
        
        user = request.user
        partner = MesUser.objects.get(id=partner_id)

        thread = models.ThreadModel.objects.create()
        thread.participants.add(request.user, partner)

        message = models.MessageModel(text=mes_text, sender=user, thread=thread)
        message.save()

        return HttpResponseRedirect('/chat/{}'.format(partner_id))

class ChatView(View):
    
    def get(self, request, partner_id):

        try:
            partner = MesUser.objects.get(id=partner_id)

        except MesUser.DoesNotExist:
            raise Http404('Пользователя не существует')

        thread = models.ThreadModel.objects.filter(
            participants=partner).filter(participants=request.user)

        if not thread:
            return HttpResponseRedirect('/chat/start_messaging/{}'.format(partner_id))

        thread = thread[0]

        messages = thread.messagemodel_set.model.objects.filter(
            thread=thread).order_by('-time')

        return render(request, 'chat_app/chat.html', {
            'partner': partner,
            'messages': messages,
            'show': 'chat',
        })

    def post(self, request, partner_id):

        try:
            partner = MesUser.objects.get(id=partner_id)

        except MesUser.DoesNotExist:
            raise Http404('Пользователя не существует')

        thread = models.ThreadModel.objects.filter(
            participants=partner).filter(participants=request.user)

        if not thread:
            return HttpResponseRedirect('/chat/start_messaging/{}'.format(partner_id))

        thread = thread[0]

        mes_text = request.POST.get('mes_text')
        message = models.MessageModel(text=mes_text, sender=request.user, thread=thread)
        message.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
