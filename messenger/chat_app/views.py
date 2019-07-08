from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.generic import TemplateView, View
from django.template.loader import render_to_string
from datetime import datetime
from auth_app.models import MesUser
from main_app.serializers import RusJsonResponse
from . import models
from .mongo import MongoDB

mongo = MongoDB()

def html_messages(request, partner=None, messages=None):
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

# --------------------- API --------------------- #
class JSONChatRedirectView(View):
    
    def get(self, request):
        address = request.META.get('HTTP_REFERER')
        id = address.split('/')[-1]
        return HttpResponseRedirect('/chat/api/{}'.format(id))


class JSONChatView(LoginRequiredMixin, View):
    
    chats_db_name = 'chats'
    login_url = '/login'
    
    def get(self, request, partner_id):
        chat = models.ChatModel.objects.filter(
            participants__id=request.user.id).filter(participants__id=partner_id)
        partner = MesUser.objects.filter(id=partner_id)
        if not partner:
            chat_page = html_messages(request)
        elif not chat:
            partner = partner[0]
            chat = models.ChatModel.objects.create(
                mongo_collection = request.user.username + '-' + partner.username,
            ).participants.add(request.user, partner)
            chat_page = html_messages(request, partner)
        else:
            chat = chat[0]
            partner = partner[0]
            messages = mongo.get_messages_from_db(self.chats_db_name, chat.mongo_collection)
            chat_page = html_messages(request, partner, messages)
        return RusJsonResponse({'chat_page': chat_page})

    def post(self, request, partner_id):
        chat = models.ChatModel.objects.filter(
            participants__id=request.user.id).filter(participants__id=partner_id)
        partner = MesUser.objects.filter(id=partner_id)
        if not partner:
            chat_page = html_messages(request)
        elif not chat:
            partner = partner[0]
            chat = models.ChatModel.objects.create(
                mongo_collection = request.user.username + '-' + partner.username,
            ).participants.add(request.user, partner)
            chat_page = html_messages(request, partner)
        else:
            chat = chat[0]
            partner = partner[0]
            message = {
                'text': request.POST.get('mes_text'),
                'time': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                'sender_id': request.user.id
            }
            mongo.add_message_to_db(self.chats_db_name, chat.mongo_collection, message)
            messages = mongo.get_messages_from_db(self.chats_db_name, chat.mongo_collection)
            chat_page = html_messages(request, partner, messages)
        return RusJsonResponse({'chat_page': chat_page})


# --------------------- Контроллеры --------------------- #
class EmptyChatView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'chat_app/chat.html'


class ChatView(LoginRequiredMixin, TemplateView):
    
    login_url = '/login'
    template_name = 'chat_app/chat.html'
    chats_db_name = 'chats'

    def post(self, request, partner_id):
        chat = models.ChatModel.objects.filter(
            participants__id=request.user.id).filter(participants__id=partner_id)
        partner = MesUser.objects.filter(id=partner_id)
        if not partner:
            chat_page = html_messages(request)
        elif not chat:
            partner = partner[0]
            chat = models.ChatModel.objects.create(
                mongo_collection = request.user.username + '-' + partner.username,
            ).participants.add(request.user, partner)
            chat_page = html_messages(request, partner)
        else:
            chat = chat[0]
            partner = partner[0]
            message = {
                'text': request.POST.get('mes_text'),
                'time': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                'sender_id': request.user.id
            }
            mongo.add_message_to_db(self.chats_db_name, chat.mongo_collection, message)
            messages = mongo.get_messages_from_db(self.chats_db_name, chat.mongo_collection)
            chat_page = html_messages(request, partner, messages)
        return RusJsonResponse({'chat_page': chat_page})
