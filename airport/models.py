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