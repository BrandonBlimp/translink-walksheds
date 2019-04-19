from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Route, Trip

# Create your views here.
def index(request):
    routes = Route.objects.order_by('route_short_name')
    selected_route = None
    trip_headsigns = Trip.objects.order_by('trip_headsign').values_list('trip_headsign', flat=True).distinct()
    template = loader.get_template('app/index.html')
    context = {
        'routes': routes,
        'selected_route': selected_route,
        'trip_headsigns': trip_headsigns
    }
    return HttpResponse(template.render(context, request))
