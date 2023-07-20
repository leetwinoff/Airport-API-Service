from django.shortcuts import render
from rest_framework import viewsets

from airport.models import CrewPosition
from airport.serializers import CrewPositionSerializer


class CrewPositionViewSet(viewsets.ModelViewSet):
    queryset = CrewPosition.objects.all()
    serializer_class = CrewPositionSerializer
