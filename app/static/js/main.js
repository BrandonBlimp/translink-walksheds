$(document).ready(function () {
    $('#routeSelector .dropdown-item').click(changeRoute);
});

function changeRoute () {
    $('#dropdownMenuButton').text($(this).text());

    var url = "/routes/"
    var routeId = 

    $.ajax({
        url: url,
        method: "GET",
        data: {
            "route_id": 6771,
        },
        dataType: "json",
        success: function (response) {
            // $('#graph-overlay').find('.graph-content').html(response);
            // $('#graph-overlay').fadeIn(300);
            // hideLoadingOverlay();
            alert("it worked kinda");
        },
        error: function () {
            alert("oops");
        }
    });
}