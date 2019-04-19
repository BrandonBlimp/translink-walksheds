from django.shortcuts import render

from rest_framework import viewsets

from app.models import Route, Trip
from .serializers import RouteSerializer, TripSerializer


class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Route.objects.order_by('route_short_name')
    serializer_class = RouteSerializer


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer