from django.urls import path
from . import views

urlpatterns = [
    path('api/<int:partner_id>', views.JSONChatView.as_view()),
    path('api', views.JSONChatRedirectView.as_view()),
    path('', views.EmptyChatView.as_view()),
    path('<int:partner_id>', views.ChatView.as_view()),
]