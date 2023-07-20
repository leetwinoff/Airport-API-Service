from django.db import models


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
        return f"From {self.source} to {self.destination} {self.distance} miles"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    row = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")

    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flight")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(null=False, blank=False)
    arrival_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"Departure: {self.departure_time}, Arrival: {self.arrival_time}"