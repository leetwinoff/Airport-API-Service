from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from airport.models import CrewPosition, Crew, Airport, Route, AirplaneType, Airplane, Flight
from airport.serializers import CrewPositionSerializer, CrewSerializer, AirportSerializer, RouteSerializer, \
    AirplaneTypeSerializer, AirplaneSerializer, FlightSerializer, FlightDetailSerializer


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
    queryset = Flight.objects.prefetch_related('airplane__airplane_type').all()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj