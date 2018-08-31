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
            return Http404()

        thread = models.ThreadModel.objects.filter(
            participants=partner).filter(participants=request.user)

        if thread.exists():
            return HttpResponseRedirect('/chat/{}'.format(partner_id))

        return render(request, 'chat_app/chat.html', {
            'partner': partner,
            'show': 'start',
        })

    def post(self, request):
        
        partner_id = request.POST.get('partner_id')
        print('\n\nPOST STARTCHAT PARTNER_ID TYPE: {}\n\n'.format(type(partner_id)))
        mes_text = request.POST.get('mes_text')
        
        user = request.user
        partner = MesUser.objects.get(id=partner_id)

        thread = models.ThreadModel.objects.create()
        thread.participants.add(request.user, partner)

        message = models.MessageModel(text=mes_text, sender=user, thread=thread)
        message.save()
        print('MESSAGE: ', message, '\n\n')

        return HttpResponseRedirect('/chat/{}'.format(partner_id))

class ChatView(View):
    
    def get(self, request, partner_id):

        try:
            partner = MesUser.objects.get(id=partner_id)

        except MesUser.DoesNotExist:
            return Http404()

        thread = models.ThreadModel.objects.filter(
            participants=partner).filter(participants=request.user)

        if not thread:
            return HttpResponseRedirect('/chat/start_messaging/{}'.format(partner_id))

        messages = thread.messagemodel_set.order_by('-time')

        return render(request, 'chat_app/chat.html', {
            'partner': partner,
            'messages': messages,
            'show': 'chat',
        })
