from django.db import transaction
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
    Route,
)


class CrewPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewPosition
        fields = (
            "id",
            "position",
        )


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
        route = Route.objects.create(
            source=source_id, destination=destination_id, **validated_data
        )
        return route

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["source"] = instance.source.name
        representation["destination"] = instance.destination.name
        representation["distance"] = f"{instance.distance} miles."
        return representation


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "brand", "model", "default_row", "default_seats_in_row")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all()
    )
    crew = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True, required=False
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "row",
            "seats_in_row",
            "airplane_type",
            "capacity",
            "crew",
        )
        read_only_fields = ("row", "seats_in_row", "capacity")

    def create(self, validated_data):
        crew_data = validated_data.pop("crew", None)
        airplane_type_instance = validated_data.pop("airplane_type")
        if crew_data:
            crew_instance = Crew.objects.filter(pk__in=[crew.id for crew in crew_data])
        else:
            crew_instance = []
        validated_data["row"] = airplane_type_instance.default_row
        validated_data["seats_in_row"] = airplane_type_instance.default_seats_in_row

        airplane = Airplane.objects.create(
            airplane_type=airplane_type_instance, **validated_data
        )
        airplane.crew.set(crew_instance)
        return airplane

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            "airplane_type"
        ] = f"{instance.airplane_type.brand} {instance.airplane_type.model}"
        crew_representation = [
            f"{crew.position}: {crew.first_name} {crew.last_name}"
            for crew in instance.crew.all()
        ]
        representation["crew"] = crew_representation
        return representation


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "available_tickets",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            "route"
        ] = f"{instance.route.source} - {instance.route.destination}"
        representation[
            "airplane"
        ] = f"{instance.airplane.airplane_type.brand} {instance.airplane.airplane_type.model}"

        departure_time_formatted = timezone.localtime(instance.departure_time).strftime(
            "%d-%m-%Y %H:%M"
        )
        arrival_time_formatted = timezone.localtime(instance.arrival_time).strftime(
            "%d-%m-%Y %H:%M"
        )
        representation["departure_time"] = departure_time_formatted
        representation["arrival_time"] = arrival_time_formatted
        return representation


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    airplane = AirplaneSerializer()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "available_tickets",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, data):
        flight = data["flight"]
        row = data["row"]
        seat = data["seat"]

        existing_ticket = Ticket.objects.filter(
            flight=flight, row=row, seat=seat
        ).first()
        if existing_ticket:
            raise serializers.ValidationError(
                "A ticket with the same row and seat on this flight already exists."
            )

        return data

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["order"] = Order.objects.create(user=user)
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "order_number", "tickets")
        read_only_fields = ("order_number", "user")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order

    def update(self, instance, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", [])
            instance = super().update(instance, validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(order=instance, **ticket_data)

            return instance
