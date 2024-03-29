from rest_framework import serializers
# Подключаем модель user
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from analize.models import Siggs


class SiggsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siggs
        fields = "__all__"

