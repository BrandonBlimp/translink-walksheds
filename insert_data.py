import csv
import datetime
from pathlib import Path
from app.models import Stop, Route, Shape

# run from Django shell: exec(open('insert_data.py').read())

def create_all():
    import_stops()
    import_routes()
    import_shapes()

def delete_all():
    print("%s: deleting all Stop entries" % datetime.datetime.now())
    Stop.objects.all().delete()
    print("%s: deleting all Route entries" % datetime.datetime.now())
    Route.objects.all().delete()
    print("%s: deleting all Shape entries" % datetime.datetime.now())
    Shape.objects.all().delete()

def import_stops():
    print("%s: importing from \'data/stops.txt\'" % datetime.datetime.now())
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
    print("%s: importing from \'data/routes.txt\'" % datetime.datetime.now())
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
        bulk_create(routes, Route)


def import_shapes():
    print("%s: importing from \'data/shapes.txt\'" % datetime.datetime.now())
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
        bulk_create(shapes, Shape)


# takes two arguments:
#   1. a list (containing objects of the same Django Model)
#   2. a reference to the model class itself
def bulk_create(models, model_class):
    time_start = datetime.datetime.now()
    print("%s: start bulk_create" % time_start)

    result = model_class.objects.bulk_create(models)

    time_finish = datetime.datetime.now()
    time_elapsed = time_finish - time_start
    print("%s: bulk_create inserted %s objects and took %s" % (time_finish, len(result), time_elapsed))

