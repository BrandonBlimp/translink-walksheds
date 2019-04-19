from rest_framework import serializers

from app.models import Route, Trip


class RouteSerializer(serializers.HyperlinkedModelSerializer):
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

class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'trip_id',
            'route',
            'service_id',
            'trip_headsign',
            'direction_id',
            'block_id',
            'shape_id',
            'wheelchair_accessible' ,
            'bikes_allowed'
        )
