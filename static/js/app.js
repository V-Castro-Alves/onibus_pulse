$(document).ready(function () {
    // Handle Step 1: Trip Form Submission
    $('#tripForm').submit(function (event) {
        event.preventDefault();
        var tripId = $('#trip_id').val();

        // Fetch route trip info
        $.post('/get_trip', { trip_id: tripId }, function (data) {
            if (data.route_data) {
                $('#routeData').html('<p><strong>Route Trip Info:</strong></p>');

                data.route_data.forEach(function (trip) {
                    $('#routeData').append('<p><strong>Trip Headsign:</strong> ' + trip.trip_headsign + '</p>');
                    $('#routeData').append('<p><strong>Direction ID:</strong> ' + trip.direction_id + '</p>');
                });

                // Show Direction ID form for Step 2
                $('#directionForm').show();
            } else {
                $('#routeData').html('<p style="color:red;">' + data.error + '</p>');
                $('#directionForm').hide(); // Ensure the next form doesn't show on error
            }
        });
    });

    // Handle Step 2: Direction Form Submission
    $('#directionForm').submit(function (event) {
        event.preventDefault();
        var directionId = $('#direction_id').val();
        var tripId = $('#trip_id').val(); // Use the same Trip ID from Step 1

        // Fetch shape stops
        $.post('/get_shape_stops', { direction_id: directionId, trip_id: tripId }, function (data) {
            if (data.shape_stops) {
                $('#shapeStops').html('<p><strong>Shape Stops:</strong></p>');

                data.shape_stops.forEach(function (stop) {
                    $('#shapeStops').append('<p>' + stop.stop_id + ' - ' + stop.stop_name + '</p>');
                });

                // Show Stop ID form for Step 3
                $('#stopForm').show();
            } else {
                $('#shapeStops').html('<p style="color:red;">' + data.error + '</p>');
                $('#stopForm').hide(); // Ensure the next form doesn't show on error
            }
        });
    });

    // Handle Step 3: Stop Form Submission
    $('#stopForm').submit(function (event) {
        event.preventDefault();
        var stopId = $('#stop_id').val();
        var tripId = $('#trip_id').val();
        var directionId = $('#direction_id').val();

        // Fetch stop times
        $.post('/get_stop_times', { stop_id: stopId, trip_id: tripId, direction_id: directionId }, function (data) {
            if (data.first_arrival_time) {
                $('#stopTimes').html('<p><strong>First Arrival Time:</strong> ' + data.first_arrival_time + '</p>');
            } else {
                $('#stopTimes').html('<p style="color:red;">' + data.error + '</p>');
            }
        });
    });
});
