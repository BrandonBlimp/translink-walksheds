from django.db import models

# Create your models here.

class Stop(models.Model):
    LOCATION_TYPE_STOP = 1
    LOCATION_TYPE_STATION = 2
    LOCATION_TYPE_STATION_ENTRANCE = 3
    LOCATION_TYPE_CHOICES = (
        (LOCATION_TYPE_STOP, 'stop'),
        (LOCATION_TYPE_STATION, "station"),
        (LOCATION_TYPE_STATION_ENTRANCE, "station entrance/exit")
    )

    stop_id = models.IntegerField(primary_key=True)
    stop_code = models.IntegerField(blank=True)
    stop_name = models.CharField(max_length=200)
    stop_lat = models.DecimalField(max_digits=9, decimal_places=6)
    stop_lon = models.DecimalField(max_digits=9, decimal_places=6)
    zone_id = models.CharField(max_length=50, blank=True)
    location_type = models.IntegerField(choices=LOCATION_TYPE_CHOICES, blank=True)

class Route(models.Model):
    ROUTE_TYPE_LRT = 0
    ROUTE_TYPE_METRO = 1
    ROUTE_TYPE_RAIL = 2
    ROUTE_TYPE_BUS = 3
    ROUTE_TYPE_FERRY = 4
    ROUTE_TYPE_CABLE_TRAM = 5
    ROUTE_TYPE_AERIAL_LIFT = 6
    ROUTE_TYPE_FUNICULAR = 7
    ROUTE_TYPE_CHOICES = (
        (ROUTE_TYPE_LRT, "Tram, Streetcar, Light rail"),
        (ROUTE_TYPE_METRO, "Subway, Metro"),
        (ROUTE_TYPE_RAIL, "Heavy Rail"),
        (ROUTE_TYPE_BUS, "Bus"),
        (ROUTE_TYPE_FERRY, "Ferry"),
        (ROUTE_TYPE_CABLE_TRAM, "Cable Tram"),
        (ROUTE_TYPE_AERIAL_LIFT, "Aerial Lift"),
        (ROUTE_TYPE_FUNICULAR, "Funicular")
    )

    route_id = models.IntegerField(primary_key=True)
    agency_id = models.CharField(max_length=20, blank=True)
    route_short_name = models.CharField(default="", max_length=10, blank=True)
    route_long_name = models.CharField(default="", max_length=100, blank=True)
    route_type = models.IntegerField(choices=ROUTE_TYPE_CHOICES)
    route_color = models.CharField(max_length=6, default="FFFFFF", blank=True)
    route_text_color = models.CharField(max_length=6, default="000000", blank=True)
