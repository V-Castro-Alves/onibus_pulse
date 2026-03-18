import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bus_provider.dart';

class ETADetailScreen extends StatefulWidget {
  const ETADetailScreen({super.key});

  @override
  State<ETADetailScreen> createState() => _ETADetailScreenState();
}

class _ETADetailScreenState extends State<ETADetailScreen> {
  @override
  void initState() {
    super.initState();
    _refreshETA();
  }

  void _refreshETA() {
    final provider = context.read<BusProvider>();
    if (provider.selectedRoute != null &&
        provider.selectedTrip != null &&
        provider.selectedStop != null) {
      provider.fetchETA(
        provider.selectedRoute!.routeId,
        provider.selectedTrip!.shapeId,
        provider.selectedStop!.stopId,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<BusProvider>();
    final stop = provider.selectedStop;

    if (stop == null) return const Scaffold(body: Center(child: Text('No stop selected')));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Real-time ETA'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshETA,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      stop.stopName,
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('Route: ${provider.selectedRoute?.routeId}'),
                    Text('Direction: ${provider.selectedTrip?.tripHeadsign}'),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Upcoming Buses',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const Divider(),
            Expanded(
              child: provider.isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : provider.currentEtas.isEmpty
                      ? const Center(
                          child: Text(
                            'No real-time data available at the moment.\nTry refreshing in a few minutes.',
                            textAlign: TextAlign.center,
                          ),
                        )
                      : ListView.builder(
                          itemCount: provider.currentEtas.length,
                          itemBuilder: (context, index) {
                            final eta = provider.currentEtas[index];
                            return Card(
                              margin: const EdgeInsets.symmetric(vertical: 8),
                              color: Colors.blue[50],
                              child: ListTile(
                                leading: const Icon(Icons.directions_bus, color: Colors.blue),
                                title: Text(
                                  'ETA: ${eta.remainingMinutes} min',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18,
                                    color: Colors.blue,
                                  ),
                                ),
                                subtitle: Text(
                                  'Scheduled: ${eta.scheduledArrival} (${eta.status})\nVehicle: ${eta.vehiclePrefix}',
                                ),
                                trailing: Text(
                                  eta.etaTime,
                                  style: const TextStyle(fontWeight: FontWeight.bold),
                                ),
                              ),
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }
}
