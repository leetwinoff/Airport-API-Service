import random
import string

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from user.models import User


class CrewPosition(models.Model):
    position = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.position


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.ForeignKey(CrewPosition, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=3, unique=True)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.FloatField()

    def __str__(self):
        return f"From {self.source} to {self.destination}. Distance: {self.distance} mi."


class AirplaneType(models.Model):
    brand = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    default_row = models.PositiveIntegerField(default=0)
    default_seats_in_row = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    row = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")
    crew = models.ManyToManyField(Crew, related_name="airplanes", blank=True)

    @property
    def capacity(self):
        return self.row * self.seats_in_row


    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flight")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(null=False, blank=False)
    arrival_time = models.DateTimeField(null=False, blank=False)

    @property
    def available_tickets(self):
        booked_tickets_count = self.tickets.count()
        return self.airplane.capacity - booked_tickets_count


    def __str__(self):
        departure_time_formatted = timezone.localtime(self.departure_time).strftime('%d-%m-%Y at %H:%M')
        arrival_time_formatted = timezone.localtime(self.arrival_time).strftime('%d-%m-%Y at %H:%M')
        return f"Departure from {self.route.source} on {departure_time_formatted}" \
               f" - Arrival to {self.route.destination} on {arrival_time_formatted}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=8, unique=True, null=False)

    class Meta:
        ordering = ["-created_at"]
        db_table = "order"


    def generate_order_number(self):
        letters = string.ascii_uppercase
        digits = string.digits[0:10]
        random_letters = "".join(random.choices(letters, k=3))
        random_digits = "".join(random.choices(digits, k=5))
        return f"{random_letters}{random_digits}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a unique order number for new instances
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order No. {self.order_number} created at {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(row, seat, flight, error_to_raise):
        airplane = flight.airplane
        if not (1 <= row <= airplane.row):
            raise error_to_raise(
                {
                    "row": f"Row number must be in available range (1, {airplane.row}): (1, {airplane.row})"
                }
            )
        if not (1 <= seat <= airplane.seats_in_row):
            raise error_to_raise(
                {
                    "seat": f"Seat number must be in available range (1, {airplane.seats_in_row}): "
                            f"(1, {airplane.seats_in_row})"
                }
            )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )



    def __str__(self):
        return f"Ticket row: {self.row} seat: {self.seat} order No. {self.order.order_number}"

