import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart';
import 'utils/theme.dart';
import 'screens/invite_generate_screen.dart';
import 'screens/invite_join_screen.dart';
import 'screens/invite_screen.dart';

void main() {
  runApp(const JustUsApp());
}

class JustUsApp extends StatelessWidget {
  const JustUsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "JustUs",
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,

      // 🔥 Starting screen
      home: const LoginScreen(),

      // Optional: If you want navigation using routes
      routes: {
        "/login": (context) => const LoginScreen(),
        "/invite-options": (context) => const InviteOptionScreen(),
        "/dashboard": (context) => const DashboardScreen(),
        "/invite-generate": (context) => const InviteGenerateScreen(),
        "/invite-join": (context) => InviteJoinScreen(),
      


      },
    );
  }
}
