import 'package:flutter/material.dart';
import '../widgets/signal_button.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Send Signal"),
      ),

      body: GridView.count(
        crossAxisCount: 2,
        padding: const EdgeInsets.all(20),
        crossAxisSpacing: 20,
        mainAxisSpacing: 20,
        children: [
          SignalButton(emoji: "❤️", label: "Love", onTap: () {}),
          SignalButton(emoji: "🥺", label: "Miss You", onTap: () {}),
          SignalButton(emoji: "🔔", label: "Reminder", onTap: () {}),
          SignalButton(emoji: "🚨", label: "Emergency", onTap: () {}),
        ],
      ),
    );
  }
}
