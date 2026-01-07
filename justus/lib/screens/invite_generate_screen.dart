import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart';
import 'invite_join_screen.dart';


class InviteGenerateScreen extends StatefulWidget {
  const InviteGenerateScreen({super.key});

  @override
  State<InviteGenerateScreen> createState() => _InviteGenerateScreenState();
}

class _InviteGenerateScreenState extends State<InviteGenerateScreen> {
  String inviteCode = "";
  Future<String?> generateInviteCode(String userId) async {
  final url = Uri.parse("https://justus-exvn.onrender.com/generate_code");

  final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"user_id": userId}),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data["invite_code"];
  } else {
    return null;
  }
}

  @override
  void initState() {
    super.initState();
    loadCode();
    
  }

  void loadCode() async {
  String? code = await generateInviteCode("USER1");
  setState(() {
    inviteCode = code ?? "ERROR";
  });
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Invite Partner")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Your Invite Code",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 20),

            Container(
              padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(14),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 10,
                  ),
                ],
              ),
              child: Text(
                inviteCode,
                style: const TextStyle(
                  fontSize: 40,
                  letterSpacing: 4,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            const SizedBox(height: 40),

            ElevatedButton(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: inviteCode));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Code Copied!")),
                );
              },
              child: const Text("Copy Code"),
            ),

            const SizedBox(height: 20),


          ],
        ),
      ),
    );
  }
}
