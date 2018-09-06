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

class ThreadApiView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):

        threads = chat_app.ThreadModel.objects.filter(
            participants=request.user).order_by('-last_message_time')

        partners = list()

        for thread in threads:

            partner = thread.get_partner(request.user)
            partners.append(partner)

        serializer = serializers.MesUserSerializer(partners, many=True)

        for user in serializer.data:
            
            thread = threads.filter(participants=user['id'])[0]
            user['last_message_text'] = thread.last_message_text
            time = thread.last_message_time
            user['last_message_time'] = ':'.join([str(time.hour + 3), str(time.minute)])

        left_chats = render_to_string(
            'main_app/left_chats.html',
            {'accounts': serializer.data},
            request
        )

        return RusJsonResponse({'left_chats': left_chats})
