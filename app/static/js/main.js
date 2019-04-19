$(document).ready(function () {

    $('#routeSelector .dropdown-item').click( function() {
        $('#dropdownMenuButton').text($(this).text());
    });

})