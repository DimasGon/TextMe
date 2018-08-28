from django.urls import path
from . import views

# Путь от корня: account/
urlpatterns = [
    path('<int:pk>', views.AccountView.as_view()),
]