from django.shortcuts import render
from rest_framework import viewsets

from airport.models import CrewPosition, Crew
from airport.serializers import CrewPositionSerializer, CrewSerializer


class CrewPositionViewSet(viewsets.ModelViewSet):
    queryset = CrewPosition.objects.all()
    serializer_class = CrewPositionSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer