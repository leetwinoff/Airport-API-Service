from django.shortcuts import render
from rest_framework import viewsets

from airport.models import CrewPosition, Crew, Airport
from airport.serializers import CrewPositionSerializer, CrewSerializer, AirportSerializer


class CrewPositionViewSet(viewsets.ModelViewSet):
    queryset = CrewPosition.objects.all()
    serializer_class = CrewPositionSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer