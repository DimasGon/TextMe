from django.urls import path
from . import views

urlpatterns = [
    path('api/<int:partner_id>', views.JSONChatView.as_view()),
    path('', views.EmptyChatView.as_view()),
    path('start_messaging/<int:partner_id>', views.StartChatView.as_view()),
    path('<int:partner_id>', views.ChatView.as_view()),
]