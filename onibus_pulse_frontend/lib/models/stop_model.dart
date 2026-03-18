class Stop {
  final String stopId;
  final String stopName;
  final int stopOrder;
  final double lat;
  final double lon;

  Stop({
    required this.stopId,
    required this.stopName,
    required this.stopOrder,
    required this.lat,
    required this.lon,
  });

  factory Stop.fromJson(Map<String, dynamic> json) {
    return Stop(
      stopId: json['stop_id'],
      stopName: json['stop_name'],
      stopOrder: json['stop_order'],
      lat: (json['lat'] as num).toDouble(),
      lon: (json['lon'] as num).toDouble(),
    );
  }
}
