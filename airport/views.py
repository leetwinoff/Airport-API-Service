from django.shortcuts import render
from rest_framework import viewsets


from airport.models import CrewPosition, Crew, Airport, Route, AirplaneType, Airplane, Flight
from airport.serializers import CrewPositionSerializer, CrewSerializer, AirportSerializer, RouteSerializer, \
    AirplaneTypeSerializer, AirplaneSerializer, FlightSerializer


class CrewPositionViewSet(viewsets.ModelViewSet):
    queryset = CrewPosition.objects.all()
    serializer_class = CrewPositionSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer