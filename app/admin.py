from django.contrib import admin

from .models import Stop, Route, Shape, Trip, StopTimes

# Register your models here.

admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(Shape)
admin.site.register(Trip)
admin.site.register(StopTimes)
