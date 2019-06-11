$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(selectRoute);
    $('#toggleWalkshedsButton').click(toggleWalksheds);
});

class Stop {
    constructor(id, lat, lon, name) {
        this.id = id;
        this.lat = parseFloat(lat);
        this.lon = parseFloat(lon);
        this.name = name;
        this.latlng = {'lat':parseFloat(lat), 'lng':parseFloat(lon)};
    }
}

function enableWalkshedsButton () {
    $('#toggleWalkshedsButton').prop('disabled', false);
}

function disableWalkshedsButton () {
    $('#toggleWalkshedsButton').prop('disabled', true);
}

function selectRoute () {
    // change text displayed on dropdown button
    $('#routeSelectorButton').text($(this).text());

    // resets destination selector
    $('#destSelector').empty();
    $('#destSelectorButton').text('Select a destination');
    $('#destSelectorButton').prop('disabled', true);

    var url = "/trips/distinct_headsigns"
    var routeId = $(this).data("route-id");

    $.ajax({
        url: url,
        method: "GET",
        data: {
            "route__route_id": routeId,
        },
        dataType: "json",
        context: this,
    }).done(function (response) {
        addDestinations(response);
    }).fail(function () {
        alert("Failed to load routes");
    });
}

function addDestinations (response) {
    $('#destSelectorButton').prop('disabled', false);
    $('#destSelector').empty();

    var len = response.length;
    for (var i=0; i<len; i++) {
        var tripHeadsign = response[i]["trip_headsign"];
        var shapeID = response[i]["shape_id"];
        var tripID = response[i]['trip_id'];
        $('#destSelector').append("<a class='dropdown-item' data-shape-id='" + shapeID + "' data-trip-id='" + tripID + "' href='#'>" + tripHeadsign + "</a>");
    }

    // add onclick method to dropdown items
    $('#destSelector .dropdown-item').click(selectDestination);
}

function selectDestination () {
    // change text displayed on dropdown button
    $('#destSelectorButton').text($(this).text());
    clearStopsAndCircles();

    var shapeURL = "/shapes/";
    var shapeID = $(this).data("shape-id");
    var stopTimesURL = "/stoptimes/";
    var tripID = $(this).data("trip-id");

    $.when(
        $.ajax({
            url: shapeURL,
            method: "GET",
            data: {
                "shape_id": shapeID,
            },
            dataType: "json",
            context: this,
        }).fail(function () {
            alert("Failed to load shapes");
        }),
        $.ajax({
            url: stopTimesURL,
            method: "GET",
            data: {
                "trip_id": tripID,
            },
            dataType: "json",
            context: this,
        }).fail(function () {
            alert("Failed to load stoptimes");
        })
    ).then(function (shapeResponse, stopTimesResponse) {
        // this code block only runs if both ajax calls were successful
        loadStops(stopTimesResponse[0]);
        drawShapes(shapeResponse[0]);
    });
}

// TODO: would be better to do one API call (like /stops?stop_id=123&stop_id=425) to avoid
// making so many ajax calls.
function loadStops (stopTimes) {
    var stopsURL = "/stops/";
    var stopID;
    var stopTime;

    var deferred;
    var deffereds = [];
    
    // create a deffered for each stop_id
    for (i=0; i < stopTimes.length; i++) {
        stopTime = stopTimes[i];
        stopID = stopTime['stop_id'];
        deffered = $.ajax({
            url: stopsURL,
            method: "GET",
            data: {
                "stop_id": stopID,
            },
            dataType: "json",
            context: this,
        }).then(function (response) {
            // this is run when deferred is resolved
            stopID = response[0]["stop_id"];
            lat = response[0]["stop_lat"];
            lon = response[0]["stop_lon"];
            name = response[0]["stop_name"];
            // store result in array
            stops.push(new Stop(stopID, lat, lon, name));
        });
        // push deffered onto array of deferreds
        deffereds.push(deffered);
    }
    // after loop, resolve deferreds
    $.when.apply($, deffereds).then(function () {
        enableWalkshedsButton();
    });

}

function toggleWalksheds () {
    if (walkshedCircles && walkshedCircles.length == 0) {
        for (var i=0; i < stops.length; i++) {
            var walkshedCircle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.20,
                center: stops[i].latlng,
                radius: 800,
            });
            walkshedCircle.setMap(map);
            walkshedCircles.push(walkshedCircle);
        }
    }
}

function drawShapes (shapes) {
    if (selectedRoute) {
        clearMapRoute();
    }
    var coords = shapes.map(function (x) {
        return {
            lat: parseFloat(x["shape_pt_lat"]),
            lng: parseFloat(x["shape_pt_lon"])};
    });
    
    selectedRoute = new google.maps.Polyline({
        path: coords,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    selectedRoute.setMap(map);
}

// clears the map of the route line
function clearMapRoute () {
    selectedRoute.setMap(null);
}

function clearStopsAndCircles () {
    stops = [];
    for (var i=0; i < walkshedCircles.length; i++) {
        walkshedCircles[i].setMap(null);
    }
    walkshedCircles = [];
    disableWalkshedsButton();
}