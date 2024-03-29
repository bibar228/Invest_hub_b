from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from analize.models import Siggs
from analize.serializers import SiggsSerializer


class SiggsViewSet(viewsets.ModelViewSet):
    queryset = Siggs.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SiggsSerializer