import 'package:flutter/material.dart';
import '../models/route_model.dart';
import '../models/trip_model.dart';
import '../models/stop_model.dart';
import '../models/eta_model.dart';
import '../services/api_service.dart';

class BusProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();

  List<RouteListItem> _allRoutes = [];
  List<RouteListItem> _filteredRoutes = [];
  bool _isLoading = false;
  String? _errorMessage;

  RouteListItem? selectedRoute;
  RouteTrip? selectedTrip;
  Stop? selectedStop;
  List<ETAInfo> currentEtas = [];

  List<RouteListItem> get filteredRoutes => _filteredRoutes;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  Future<void> fetchRoutes() async {
    _setLoading(true);
    try {
      _allRoutes = await _apiService.getFlatRoutes();
      _filteredRoutes = List.from(_allRoutes);
      _errorMessage = null;
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _setLoading(false);
    }
  }

  void filterRoutes(String query) {
    if (query.isEmpty) {
      _filteredRoutes = List.from(_allRoutes);
    } else {
      _filteredRoutes = _allRoutes
          .where((route) =>
              route.routeId.toLowerCase().contains(query.toLowerCase()) ||
              route.routeLongName.toLowerCase().contains(query.toLowerCase()))
          .toList();
    }
    notifyListeners();
  }

  Future<List<RouteTrip>> getTrips(String routeId) async {
    return await _apiService.getRouteTrips(routeId);
  }

  Future<List<Stop>> getStops(String shapeId) async {
    return await _apiService.getShapeStops(shapeId);
  }

  Future<void> fetchETA(String routeId, String shapeId, String stopId) async {
    _setLoading(true);
    try {
      currentEtas = await _apiService.getETA(routeId, shapeId, stopId);
      _errorMessage = null;
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _setLoading(false);
    }
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  void selectRoute(RouteListItem route) {
    selectedRoute = route;
    selectedTrip = null;
    selectedStop = null;
    currentEtas = [];
    notifyListeners();
  }

  void selectTrip(RouteTrip trip) {
    selectedTrip = trip;
    selectedStop = null;
    currentEtas = [];
    notifyListeners();
  }

  void selectStop(Stop stop) {
    selectedStop = stop;
    notifyListeners();
  }
}
