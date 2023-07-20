from rest_framework import serializers

from airport.models import (
    CrewPosition,
    Crew, Airport,
    Airplane,
    AirplaneType,
    Ticket,
    Order,
    Flight,
    Route
)


class CrewPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewPosition
        fields = ("position",)