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

        serializer = serializers.ThreadSerializer(threads, many=True)

        print('\n\n', serializer)

        return HttpResponse(json.dumps(serializer.data))
