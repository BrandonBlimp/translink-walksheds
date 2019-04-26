from django.shortcuts import render

from rest_framework import viewsets

from app.models import Route, Trip, Shape
from .serializers import RouteSerializer, TripSerializer, ShapeSerializer


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows routes to be viewed or edited.
    """
    queryset = Route.objects.order_by('route_short_name')
    serializer_class = RouteSerializer
    filterset_fields = ('route_id',)


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class ShapeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
