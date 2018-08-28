from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmptyChatView.as_view()),
    # path('<int:pk>', views.ChatView.as_view())
]