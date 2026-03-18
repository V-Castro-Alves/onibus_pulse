class ETAInfo {
  final String vehiclePrefix;
  final String scheduledArrival;
  final int delaySeconds;
  final String etaTime;
  final int remainingMinutes;
  final String status;

  ETAInfo({
    required this.vehiclePrefix,
    required this.scheduledArrival,
    required this.delaySeconds,
    required this.etaTime,
    required this.remainingMinutes,
    required this.status,
  });

  factory ETAInfo.fromJson(Map<String, dynamic> json) {
    return ETAInfo(
      vehiclePrefix: json['vehicle_prefix'],
      scheduledArrival: json['scheduled_arrival'],
      delaySeconds: json['delay_seconds'],
      etaTime: json['eta_time'],
      remainingMinutes: json['remaining_minutes'],
      status: json['status'],
    );
  }
}
