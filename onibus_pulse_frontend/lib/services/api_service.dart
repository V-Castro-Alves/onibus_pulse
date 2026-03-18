import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/route_model.dart';
import '../models/trip_model.dart';
import '../models/stop_model.dart';
import '../models/eta_model.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator to reach localhost
  // Use localhost for iOS Simulator or Web/Desktop
  static const String baseUrl = 'http://10.0.2.2:8000'; 
  // static const String baseUrl = 'http://localhost:8000';

  Future<List<RouteListItem>> getFlatRoutes() async {
    final response = await http.get(Uri.parse('$baseUrl/routes/list'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => RouteListItem.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load routes');
    }
  }

  Future<List<RouteTrip>> getRouteTrips(String routeId) async {
    final response = await http.get(Uri.parse('$baseUrl/routes/$routeId'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => RouteTrip.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load trips for route $routeId');
    }
  }

  Future<List<Stop>> getShapeStops(String shapeId) async {
    final response = await http.get(Uri.parse('$baseUrl/stops/$shapeId'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => Stop.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load stops for shape $shapeId');
    }
  }

  Future<List<ETAInfo>> getETA(String routeId, String shapeId, String stopId) async {
    final response = await http.get(Uri.parse('$baseUrl/eta/$routeId/$shapeId/$stopId'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => ETAInfo.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load ETA');
    }
  }
}
