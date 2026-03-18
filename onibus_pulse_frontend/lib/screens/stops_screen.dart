import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bus_provider.dart';
import '../models/stop_model.dart';
import 'eta_detail_screen.dart';

class StopsScreen extends StatelessWidget {
  const StopsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<BusProvider>();
    final trip = provider.selectedTrip;

    if (trip == null) return const Scaffold(body: Center(child: Text('No direction selected')));

    return Scaffold(
      appBar: AppBar(
        title: Text('${trip.tripHeadsign} - Stops'),
      ),
      body: FutureBuilder<List<Stop>>(
        future: provider.getStops(trip.shapeId),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final stops = snapshot.data ?? [];
          if (stops.isEmpty) {
            return const Center(child: Text('No stops found for this direction.'));
          }

          return ListView.builder(
            itemCount: stops.length,
            itemBuilder: (context, index) {
              final stop = stops[index];
              return ListTile(
                leading: CircleAvatar(
                  backgroundColor: Colors.grey[200],
                  foregroundColor: Colors.blue[900],
                  radius: 12,
                  child: Text(
                    '${index + 1}',
                    style: const TextStyle(fontSize: 10),
                  ),
                ),
                title: Text(stop.stopName),
                subtitle: Text('ID: ${stop.stopId}'),
                trailing: const Icon(Icons.timer_outlined, color: Colors.green),
                onTap: () {
                  provider.selectStop(stop);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const ETADetailScreen()),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}
