import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bus_provider.dart';
import '../models/trip_model.dart';
import 'stops_screen.dart';

class TripsScreen extends StatelessWidget {
  const TripsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<BusProvider>();
    final route = provider.selectedRoute;

    if (route == null) return const Scaffold(body: Center(child: Text('No route selected')));

    return Scaffold(
      appBar: AppBar(
        title: Text('${route.routeId} - Directions'),
      ),
      body: FutureBuilder<List<RouteTrip>>(
        future: provider.getTrips(route.routeId),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final trips = snapshot.data ?? [];
          if (trips.isEmpty) {
            return const Center(child: Text('No directions found for this route.'));
          }

          return ListView.builder(
            itemCount: trips.length,
            itemBuilder: (context, index) {
              final trip = trips[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  leading: Icon(
                    trip.directionId == 0 ? Icons.arrow_forward : Icons.arrow_back,
                    color: Colors.blue,
                  ),
                  title: Text(trip.tripHeadsign),
                  subtitle: Text('Shape ID: ${trip.shapeId}'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    provider.selectTrip(trip);
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const StopsScreen()),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
