from rest_framework import serializers

from app.models import Route, Trip, Shape, StopTime, Stop


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            'route_id',
            'agency_id',
            'route_short_name',
            'route_long_name',
            'route_type',
            'route_color',
            'route_text_color'
            )

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'trip_id',
            'route',
            'service_id',
            'trip_headsign',
            'direction_id',
            # 'block_id',
            'shape_id'
            # 'wheelchair_accessible',
            # 'bikes_allowed'
        )

class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = (
            'shape_id',
            'shape_pt_lat',
            'shape_pt_lon',
            'shape_pt_sequence',
            'shape_dist_traveled'
        )

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = (
            'stop_id',
            'stop_name',
            'stop_lat',
            'stop_lon'
        )

class StopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTime
        fields = (
            'trip_id',
            'stop_id',
            'arrival_time',
            'departure_time'
        )