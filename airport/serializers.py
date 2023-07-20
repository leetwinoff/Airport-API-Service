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


class CrewSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=CrewPosition.objects.all())

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")

    def create(self, validated_data):
        position_id = validated_data.pop("position")
        crew = Crew.objects.create(position=position_id, **validated_data)
        return crew


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "code", "closest_big_city")