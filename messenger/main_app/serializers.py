from rest_framework import serializers
import chat_app.models as chat_app

class ThreadSerializer(serializers.ModelSerializer):

    class Meta:

        model = chat_app.ThreadModel
        fields = '__all__'
