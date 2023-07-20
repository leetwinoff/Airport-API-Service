from rest_framework import serializers

from airport.models import (
    CrewPosition,
    Crew,
    Airport,
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


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())
    destination = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def create(self, validated_data):
        source_id = validated_data.pop("source")
        destination_id = validated_data.pop("destination")
        route = Route.objects.create(source=source_id, destination=destination_id, **validated_data)
        return route

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['source'] = instance.source.name
        representation['destination'] = instance.destination.name
        return representation


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")