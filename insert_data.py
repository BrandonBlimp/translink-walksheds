import csv
from datetime import datetime, timedelta
from pathlib import Path

from app.models import Route, Shape, Stop, StopTime, Trip

# run from Django shell: exec(open('insert_data.py').read())

def create_all():
    st_all = datetime.now()
    import_stops()
    import_routes()
    import_shapes()
    import_trips()
    import_stoptimes()
    ft_all = datetime.now()
    et_all = ft_all - st_all
    print("%s: object creation completed after %s" % (ft_all, et_all))

def delete_all():
    print("%s: deleting all Stop entries" % datetime.now())
    Stop.objects.all().delete()
    print("%s: deleting all Route entries" % datetime.now())
    Route.objects.all().delete()
    print("%s: deleting all Shape entries" % datetime.now())
    Shape.objects.all().delete()
    print("%s: deleting all Trip entries" % datetime.now())
    Trip.objects.all().delete()
    print("%s: deleting all StopTime entries" % datetime.now())
    StopTime.objects.all().delete()

def import_stops():
    time_start = datetime.now()
    print("%s: importing from \'data/stops.txt\'" % datetime.now())
    with open(Path('data/stops.txt')) as f:
        reader = csv.reader(f, delimiter=',')
        stops = [
            Stop(
                stop_id = row[0],
                stop_code = row[1],
                stop_name = row[2],
                stop_lat = row[4],
                stop_lon = row[5],
                zone_id = row[6],
            )
            for row in reader
        ]
        import_print_helper(time_start, "stops.txt")
        # using get_or_create() is way too slow, bulk_create is needed for data of this size
        bulk_create(stops, Stop)
        # for row in reader:
        #     obj, created = Stop.objects.get_or_create(
        #         stop_id = row[0],
        #         stop_code = row[1],
        #         stop_name = row[2],
        #         stop_lat = row[4],
        #         stop_lon = row[5],
        #         zone_id = row[6],
        #         location_type = row[8]
        #         )
        #     # print(",".join([row[0], row[2]]))
        #     print(obj)
            # creates a tuple of the new object or
            # current object and a boolean of if it was created

def import_routes():
    time_start = datetime.now()
    print("%s: importing from \'data/routes.txt\'" % datetime.now())
    with open(Path('data/routes.txt')) as f:
        reader = csv.reader(f, delimiter=',')
        routes = [
            Route(
                route_id = row[0],
                agency_id = row[1],
                route_short_name = row[2],
                route_long_name = row[3],
                route_type = row[5],
                route_color = row[7],
                route_text_color = row[8]
            )
            for row in reader
        ]
        import_print_helper(time_start, "routes.txt")
        bulk_create(routes, Route)


def import_shapes():
    time_start = datetime.now()
    print("%s: importing from \'data/shapes.txt\'" % datetime.now())
    with open(Path('data/shapes.txt')) as f:
        reader = csv.reader(f, delimiter=',')
        shapes = [
            Shape(
                shape_id = row[0],
                shape_pt_lat = row[1],
                shape_pt_lon = row[2],
                shape_pt_sequence = row[3],
                shape_dist_traveled = row[4]
            )
            for row in reader
        ]
        import_print_helper(time_start, "shapes.txt")
        bulk_create(shapes, Shape)


def import_trips():
    time_start = datetime.now()
    print("%s: importing from \'data/trips.txt\'" % time_start)
    with open(Path('data/trips.txt')) as f:
        reader = csv.reader(f, delimiter=',')
        trips = [
            Trip(
                trip_id = row[2],
                route = Route.objects.get(route_id=row[0]),
                service_id = row[1],
                trip_headsign = row[3],
                direction_id = row[5],
                block_id = row[6],
                shape_id = row[7],
                wheelchair_accessible = row[8],
                bikes_allowed = row[9]
            )
            for row in reader
        ]
        import_print_helper(time_start, "trips.txt")
        bulk_create(trips, Trip)


def import_stoptimes():
    time_start = datetime.now()
    print("%s: importing from \'data/stop_times.txt\'" % time_start)
    with open(Path('data/stop_times.txt')) as f:
        reader = csv.reader(f, delimiter=',')
        stoptimes = [
            StopTime(
                # TODO: figure out a fast way to take better advantage of Djano ORM using the commented line below.
                #       The problem is that when I import the data, I have to do a database access for EVERY StopTime
                #       entry if I want to use ForeignKey
                # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
                trip_id = row[0],
                arrival_time = convert_to_datetime(row[1]),
                departure_time = convert_to_datetime(row[2]),
                stop_id = row[3],
                # stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
                stop_sequence = row[4],
                stop_headsign = row[5],
                pickup_type = row[6],
                drop_off_type = row[7],
                shape_dist_traveled = row[8] if row[8] else None
            )
            for row in reader
        ]
        import_print_helper(time_start, "stop_times.txt")
        bulk_create(stoptimes, StopTime)
        # bulk_create(stoptimes, StopTime)


# takes two arguments:
#   1. a list (containing objects of the same Django Model)
#   2. a reference to the model class itself
def bulk_create(models, model_class):
    time_start = datetime.now()
    print("%s: start bulk_create" % time_start)

    result = model_class.objects.bulk_create(models)

    time_finish = datetime.now()
    time_elapsed = time_finish - time_start
    print("%s: bulk_create inserted %s objects and took %s" % (time_finish, len(result), time_elapsed))


def import_print_helper(t_start, file_str):
    t_now = datetime.now()
    print("%s: %s import completed after %s" % (t_now, file_str, t_now - t_start))


# returns str in form 'HH:MM:SS' to datetime. datetime functions cannot be used because HH in the
# provided data can exceed 24
def convert_to_datetime(str):
    hrs, mins, secs = str.split(":")
    return timedelta(seconds=int(secs), minutes=int(mins), hours=int(hrs))
