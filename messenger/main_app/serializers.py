from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework import serializers
import chat_app.models as chat_app

class RusJsonResponse(JsonResponse):

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=False, *args, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, *args, **kwargs)


class MesUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = chat_app.MesUser
        fields = ('id', 'first_name', 'second_name', 'avatar')
