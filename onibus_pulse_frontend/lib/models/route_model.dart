class RouteListItem {
  final String routeId;
  final String routeLongName;
  final String stationName;
  final List<String> serviceId;

  RouteListItem({
    required this.routeId,
    required this.routeLongName,
    required this.stationName,
    required this.serviceId,
  });

  factory RouteListItem.fromJson(Map<String, dynamic> json) {
    return RouteListItem(
      routeId: json['route_id'],
      routeLongName: json['route_long_name'],
      stationName: json['station_name'],
      serviceId: List<String>.from(json['service_id']),
    );
  }
}

class StationRoutes {
  final String stationName;
  final List<RouteListItem> routes;

  StationRoutes({
    required this.stationName,
    required this.routes,
  });

  factory StationRoutes.fromJson(Map<String, dynamic> json) {
    return StationRoutes(
      stationName: json['station_name'],
      routes: (json['routes'] as List)
          .map((r) => RouteListItem.fromJson(r))
          .toList(),
    );
  }
}
