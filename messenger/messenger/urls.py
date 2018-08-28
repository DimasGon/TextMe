from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts_app.urls')),
    path('chats/', include('chat_app.urls')),
    path('', include('auth_app.urls')),
    path('', include('main_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
