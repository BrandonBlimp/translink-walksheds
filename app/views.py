from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Route

# Create your views here.
def index(request):
    route_list = Route.objects.all()
    template = loader.get_template('app/index.html')
    context = {
        'route_list': route_list
    }
    return HttpResponse(template.render(context, request))
