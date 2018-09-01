from rest_framework import serializers
import chat_app.models as chat_app

class MesUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = chat_app.MesUser
        fields = ('id', 'first_name', 'second_name', 'avatar')
