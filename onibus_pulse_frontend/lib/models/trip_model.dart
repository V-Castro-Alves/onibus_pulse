class RouteTrip {
  final String tripId;
  final String tripHeadsign;
  final String shapeId;
  final int directionId;

  RouteTrip({
    required this.tripId,
    required this.tripHeadsign,
    required this.shapeId,
    required this.directionId,
  });

  factory RouteTrip.fromJson(Map<String, dynamic> json) {
    return RouteTrip(
      tripId: json['trip_id'],
      tripHeadsign: json['trip_headsign'],
      shapeId: json['shape_id'],
      directionId: json['direction_id'],
    );
  }
}
