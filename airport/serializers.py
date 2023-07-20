from django.utils import timezone

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
        representation["source"] = instance.source.name
        representation["destination"] = instance.destination.name
        return representation


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "brand", "model", "default_row", "default_seats_in_row")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(queryset=AirplaneType.objects.all())

    class Meta:
        model = Airplane
        fields = ("id", "name", "row", "seats_in_row", "airplane_type")
        read_only_fields = ("row", "seats_in_row")

    def create(self, validated_data):
        airplane_type_instance = validated_data.pop("airplane_type")
        validated_data["row"] = airplane_type_instance.default_row
        validated_data["seats_in_row"] = airplane_type_instance.default_seats_in_row
        airplane = Airplane.objects.create(airplane_type=airplane_type_instance, **validated_data)
        return airplane

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["airplane_type"] = f"{instance.airplane_type.brand} {instance.airplane_type.model}"
        return representation


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["route"] = f"{instance.route.source} - {instance.route.destination}"
        representation["airplane"] = instance.airplane.name

        departure_time_formatted = timezone.localtime(instance.departure_time).strftime('%d-%m-%Y %H:%M')
        arrival_time_formatted = timezone.localtime(instance.arrival_time).strftime('%d-%m-%Y %H:%M')
        representation["departure_time"] = departure_time_formatted
        representation["arrival_time"] = arrival_time_formatted
        return representation
