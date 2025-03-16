from django.db import models

class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name