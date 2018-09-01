from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, View
import chat_app.models as chat_app
import json
from . import serializers

class IndexView(TemplateView):
    template_name = 'main_app/index.html'

class ThreadApiView(View):

    def get(self, request):

        threads = chat_app.ThreadModel.objects.filter(
            participants=request.user).order_by('-last_message_time')

        partners = list()

        for thread in threads:

            partner = thread.get_partner(request.user)
            partners.append(partner)

        serializer = serializers.MesUserSerializer(partners, many=True)

        return HttpResponse(serializer.data)
