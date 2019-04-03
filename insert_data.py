import csv

from pathlib import Path
from app.models import Stop

# run from shell: exec(open('insert_data.py').read())

def import_stops():
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
            Stop.objects.bulk_create(stops)
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
