import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;


class InviteJoinScreen extends StatelessWidget {
  InviteJoinScreen({super.key});

  final TextEditingController codeController = TextEditingController();
  
  Future<bool> joinPartner(String code, String userId) async {
  final url = Uri.parse("https://justus-exvn.onrender.com/join_code");

  final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({
      "code": code,
      "user_id": userId,
    }),
  );

  return response.statusCode == 200;
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Join Partner")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const SizedBox(height: 30),

            const Text(
              "Enter Invite Code",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 20),

            TextField(
              controller: codeController,
              decoration: InputDecoration(
                hintText: "Invite Code",
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),

            const SizedBox(height: 30),

            ElevatedButton(
              onPressed: () async {
                bool success = await joinPartner(codeController.text.trim(), "USER2");

                if (success) {
                  Navigator.pushNamed(context, "/dashboard");
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Invalid Code")),
                  );
                }
              },

              child: const Text("Connect"),
            ),
          ],
        ),
      ),
    );
  }
}
