from django.shortcuts import render

from app.models import Route, Shape, Stop, StopTime, Trip
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .serializers import (RouteSerializer, ShapeSerializer, StopSerializer,
                          StopTimeSerializer, TripSerializer)


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows routes to be viewed
    """
    queryset = Route.objects.order_by('route_short_name')
    serializer_class = RouteSerializer
    filterset_fields = ('route_id',)


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trips to be viewed
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filterset_fields = ('route__route_id',)

    # this decorator allows routing to the distinct_headsigns method
    # access this method with the URL /trips/distinct_headsigns/
    # NOTE: the .distinct() method ONLY WORKS IF DATABASE IS POSTGRES
    @list_route()
    def distinct_headsigns(self, request):
        query_set = self.filter_queryset(self.get_queryset().distinct('trip_headsign'))
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)

class ShapeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trips to be viewed
    """
    queryset = Shape.objects.all().order_by("shape_pt_sequence")
    serializer_class = ShapeSerializer
    pagination_class = None
    filterset_fields = ('shape_id',)

class StopViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Stops to be viewed
    """
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filterset_fields = ('stop_id',)

class StopTimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StopTimes to be viewed
    """
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer
    filterset_fields = ('trip_id',)
