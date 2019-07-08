from django.contrib import admin
from . import models


@admin.register(models.MongoServerModel)
class MongoServerAdmin(admin.ModelAdmin):
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.ChatModel)
class ChatAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
