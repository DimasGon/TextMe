from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from main_app.serializers import RusJsonResponse
import chat_app.models as chat_app
import json
from . import serializers

class IndexView(TemplateView):
    template_name = 'main_app/index.html'

class ChatsApiView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):
        chats = chat_app.ChatModel.objects.filter(
            participants=request.user).order_by('-last_message_time')
        partners = list()
        for chat in chats:
            partner = chat.get_partner(request.user)
            partners.append(partner)
        serializer = serializers.MesUserSerializer(partners, many=True)
        for user in serializer.data:
            chat = chats.filter(participants=user['id'])[0]
            user['last_message_text'] = chat.last_message_text
            time = chat.last_message_time
            print(time)
            user['last_message_time'] = time
        print(serializer.data)
        left_chats = render_to_string(
            'main_app/left_chats.html',
            {'accounts': serializer.data},
            request
        )
        return RusJsonResponse({'left_chats': left_chats})
