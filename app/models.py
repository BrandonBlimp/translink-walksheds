from django.db import models

# See the Google GTFS documentation for details
# https://developers.google.com/transit/gtfs/reference/

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
    stop_code = models.CharField(max_length=10, blank=True, default="")
    stop_name = models.CharField(max_length=200)
    stop_lat = models.DecimalField(max_digits=9, decimal_places=6)
    stop_lon = models.DecimalField(max_digits=9, decimal_places=6)
    zone_id = models.CharField(max_length=50, blank=True)
    location_type = models.IntegerField(choices=LOCATION_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return ",".join([str(self.stop_id), self.stop_name])

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

    def __str__(self):
        return ",".join([str(self.route_id), self.route_short_name, self.route_long_name])


class Shape(models.Model):
    shape_id = models.CharField(max_length=20)
    shape_pt_lat = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_lon = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_sequence = models.PositiveIntegerField()
    shape_dist_traveled = models.FloatField()

    def __str__(self):
        return ",".join([self.shape_id, str(self.shape_pt_lat), str(self.shape_pt_lon)])


class Trip(models.Model):
    DIRECTION_ID_CHOICES = (
        (0,"direction 0"),
        (1,"direction 1")
    )

    WHEELCHAIR_ACCESSIBLE_UNKNOWN = 0
    WHEELCHAIR_ACCESSIBLE_YES = 1
    WHEELCHAIR_ACCESSIBLE_NO = 2
    WHEELCHAIR_ACCESSIBLE_CHOICES = (
        (WHEELCHAIR_ACCESSIBLE_UNKNOWN, "No accessibility info"),
        (WHEELCHAIR_ACCESSIBLE_YES, "Wheelchair-accessible"),
        (WHEELCHAIR_ACCESSIBLE_NO, "Not wheelchair-accessible")
    )

    BIKES_ALLOWED_UNKNOWN = 0
    BIKES_ALLOWED_YES = 1
    BIKES_ALLOWED_NO = 2
    BIKES_ALLOWED_CHOICES = (
        (BIKES_ALLOWED_UNKNOWN, "No bike info"),
        (BIKES_ALLOWED_YES, "Bikes allowed"),
        (BIKES_ALLOWED_NO, "Bikes not allowed")
    )

    trip_id = models.CharField(max_length=20, primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=10)
    trip_headsign = models.CharField(max_length=100, blank=True)
    direction_id = models.IntegerField(choices=DIRECTION_ID_CHOICES)
    block_id = models.CharField(max_length=100, blank=True)
    shape_id = models.CharField(max_length=20, blank=True, null=True)
    wheelchair_accessible = models.IntegerField(choices=WHEELCHAIR_ACCESSIBLE_CHOICES, default=0, blank=True,)
    bikes_allowed = models.IntegerField(choices=BIKES_ALLOWED_CHOICES, default=0, blank=True)

    def __str__(self):
        return ",".join([self.trip_id, self.trip_headsign])

class StopTime(models.Model):
    PICKUP_TYPE_REGULAR = 0
    PICKUP_TYPE_NONE = 1
    PICUKP_TYPE_PHONE_REQUEST = 2
    PICKUP_TYPE_DRIVER_COORD = 3
    PICKUP_TYPE_CHOICES = (
        (PICKUP_TYPE_REGULAR, "Regularly scheduled pickup"),
        (PICKUP_TYPE_NONE, "No pickup available"),
        (PICUKP_TYPE_PHONE_REQUEST, "Phone agency to arrange pickup"),
        (PICKUP_TYPE_DRIVER_COORD, "Coordinate with driver to arrange pickup")
    )

    DROPOFF_TYPE_REGULAR = 0
    DROPOFF_TYPE_NONE = 1
    PICUKP_TYPE_PHONE_REQUEST = 2
    DROPOFF_TYPE_DRIVER_COORD = 3
    DROPOFF_TYPE_CHOICES = (
        (DROPOFF_TYPE_REGULAR, "Regularly scheduled drop off"),
        (DROPOFF_TYPE_NONE, "No drop off available"),
        (PICUKP_TYPE_PHONE_REQUEST, "Phone agency to arrange drop off"),
        (DROPOFF_TYPE_DRIVER_COORD, "Coordinate with driver to arrange drop off")
    )

    # TODO: figure out a fast way to take better advantage of Djano ORM using the commented line below.
    #       The problem is that when I import the data, I have to do a database access for EVERY StopTime
    #       entry if I want to use ForeignKey
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=20)
    arrival_time = models.DurationField()
    departure_time = models.DurationField()
    stop_id = models.IntegerField()
    # stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.PositiveIntegerField()
    stop_headsign = models.CharField(max_length=100, blank=True)
    pickup_type = models.IntegerField(choices=PICKUP_TYPE_CHOICES, default=PICKUP_TYPE_REGULAR, blank=True)
    drop_off_type = models.IntegerField(choices=DROPOFF_TYPE_CHOICES, default=PICKUP_TYPE_REGULAR, blank=True)
    shape_dist_traveled = models.FloatField(blank=True, null=True)

    def __str__(self):
        return ",".join([self.trip_id, str(self.arrival_time), str(self.departure_time)])