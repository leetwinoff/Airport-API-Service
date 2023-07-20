from django.db import models


class CrewPosition(models.Model):
    position = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.position