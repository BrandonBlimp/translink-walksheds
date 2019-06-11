$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(selectRoute);
    $('#toggleWalkshedsButton').click(toggleWalksheds);
});

function toggleWalksheds () {
    
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
        loadDestinations(response);
    }).fail(function () {
        alert("Failed to load routes");
    });
}

function loadDestinations (response) {
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

    var url = "/shapes/"
    var shapeID = $(this).data("shape-id");

    $.ajax({
        url: url,
        method: "GET",
        data: {
            "shape_id": shapeID,
        },
        dataType: "json",
        context: this,
    }).done(function (response) {
        drawShapes(response);
    }).fail(function () {
        alert("Failed to load trips");
    });
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