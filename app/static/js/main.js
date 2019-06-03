$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(changeRoute);
});

function changeRoute () {
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
            changeDestinations(response);
        },
        error: function () {
            alert("oops");
        }
    });
}

function changeDestinations (response) {
    $('#destSelectorButton').prop('disabled', false);
    $('#destSelector').empty();

    var len = response.length;
    for (var i=0; i<len; i++) {
        var tripHeadsign = response[i]["trip_headsign"]
        $('#destSelector').append("<a class='dropdown-item' href='#'>" + tripHeadsign + "</a>");
    }
}