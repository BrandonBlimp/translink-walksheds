$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(changeRoute);
});

function changeRoute () {
    $('#routeSelectorButton').text($(this).text());

    var url = "/routes/"
    var routeId = $(this).data("route-id");

    $.ajax({
        url: url,
        method: "GET",
        data: {
            "route_id": routeId,
        },
        dataType: "json",
        success: function (response) {
            // $('#graph-overlay').find('.graph-content').html(response);
            // $('#graph-overlay').fadeIn(300);
            // hideLoadingOverlay();
            alert(routeId);
        },
        error: function () {
            alert("oops");
        }
    });
}