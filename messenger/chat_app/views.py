from django.shortcuts import render
from django.views.generic import TemplateView

class EmptyChatView(TemplateView):
    template_name = 'chat_app/chat.html'
