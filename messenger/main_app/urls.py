from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('chats_api', views.ThreadApiView.as_view()),
]
