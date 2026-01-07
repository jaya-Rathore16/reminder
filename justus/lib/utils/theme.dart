import 'package:flutter/material.dart';

class AppTheme {
  static Color primary = const Color(0xffFF4F6D);
  static Color bg = const Color(0xffFFF4F6);

  static ThemeData lightTheme = ThemeData(
    fontFamily: 'Poppins',
    primaryColor: primary,
    scaffoldBackgroundColor: bg,
    appBarTheme: AppBarTheme(
      backgroundColor: primary,
      elevation: 0,
      titleTextStyle: const TextStyle(
        color: Colors.white,
        fontSize: 20,
        fontWeight: FontWeight.w600,
      ),
    ),
  );
}
