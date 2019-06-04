$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(selectRoute);
});

function selectRoute () {
    // change text displayed on dropdown button
    $('#routeSelectorButton').text($(this).text());

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
        success: function (response) {
            loadDestinations(response);
        },
        error: function () {
            alert("oops");
        }
    });
}

function loadDestinations (response) {
    $('#destSelectorButton').prop('disabled', false);
    $('#destSelector').empty();

    var len = response.length;
    for (var i=0; i<len; i++) {
        var tripHeadsign = response[i]["trip_headsign"];
        var shapeID = response[i]["shape_id"];
        $('#destSelector').append("<a class='dropdown-item' data-shape-id='" + shapeID + "' href='#'>" + tripHeadsign + "</a>");
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
        success: function (response) {
            drawShapes(response);
        },
        error: function () {
            alert("oops");
        }
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