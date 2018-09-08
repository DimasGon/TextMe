from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from auth_app.models import MesUser
from django.template.loader import render_to_string
from main_app.serializers import RusJsonResponse
from . import models

# --------------------- API --------------------- #
class JSONChatRedirectView(View):
    
    def get(self, request):

        adress = request.META.get('HTTP_REFERER')
        id = int(adress[adress.find('chat/') + 5])

        return HttpResponseRedirect('/chat/api/{}'.format(id))

class JSONChatView(LoginRequiredMixin, View):

    login_url = '/login'

    def html_messages(self, request, partner=None, messages=None):

        if messages:
            chat_page = render_to_string(
                'chat_app/json_chat.html',
                {
                    'partner': partner,
                    'messages': messages,
                    'show': 'chat',
                },
                request
            )

        elif partner:
            chat_page = render_to_string(
                'chat_app/json_chat.html', 
                {
                    'partner': partner,
                    'show': 'start',
                },
                request
            )

        else:
            chat_page = render_to_string(
                'chat_app.json_chat.html',
                {'error': 'Запрашиваемого пользователя не существует!'},
                request
            )

        return chat_page

    def get(self, request, partner_id):
        
        try:
            partner = MesUser.objects.get(id=partner_id)

        except MesUser.DoesNotExist:
            
            chat_page = self.html_messages(request)

            return RusJsonResponse({'chat_page': chat_page})

        thread = models.ThreadModel.objects.filter(
            participants=partner).filter(participants=request.user)

        if not thread:
            
            chat_page = self.html_messages(request, partner)

            return RusJsonResponse({'chat_page': chat_page})

        thread = thread[0]

        messages = thread.messagemodel_set.model.objects.filter(
            thread=thread).order_by('-time')

        chat_page = self.html_messages(request, partner, messages)

        return RusJsonResponse({'chat_page': chat_page})

# --------------------- Контроллеры --------------------- #
class EmptyChatView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'chat_app/chat.html'

class StartChatView(LoginRequiredMixin, View):
    
    login_url = '/login'

    def post(self, request, partner_id):
        
        mes_text = request.POST.get('mes_text')
        image = request.POST.get('image')
        
        user = request.user
        partner = MesUser.objects.get(id=partner_id)

        thread = models.ThreadModel.objects.create()
        thread.participants.add(request.user, partner)

        message = models.MessageModel(text=mes_text, sender=user, 
            thread=thread, image=image)
        message.save()

        return HttpResponseRedirect('/chat/api/{}'.format(partner_id))

class ChatView(LoginRequiredMixin, TemplateView):
    
    login_url = '/login'
    template_name = 'chat_app/chat.html'

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
        image = request.FILES.get('image')
        message = models.MessageModel(text=mes_text, sender=request.user,
            thread=thread, image=image)
        message.save()

        return HttpResponseRedirect('/chat/api/{}'.format(partner_id))
]