import os
import json
import random
import string
from flask import Flask, request, jsonify, render_template_string
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# --- FIREBASE SETUP ---
firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')

if firebase_creds:
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
else:
    # Local testing ke liye file honi chahiye
    if os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
    else:
        cred = None # Error handle karne ke liye

if cred and not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://justus-bd376-default-rtdb.firebaseio.com/'
    })

# --- HELPER FUNCTIONS ---
def generate_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))

# --- HTML UI FOR TESTING (Ye naya hai) ---
TEST_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JustUs Tester</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; max-width: 600px; margin: auto; background: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
        input, button { width: 100%; padding: 10px; margin-top: 10px; box-sizing: border-box; }
        button { background: #ff4081; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #e91e63; }
        h2 { margin-top: 0; color: #333; }
        pre { background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
        .status { font-weight: bold; color: green; margin-top: 10px; }
    </style>
</head>
<body>
    <h1 style="text-align:center; color:#ff4081;">❤️ JustUs Live Test ❤️</h1>
    
    <div class="card">
        <h2>1. Pehle Apna Naam Rakho</h2>
        <input type="text" id="myId" placeholder="Enter Your Name (Unique ID)">
        <p style="font-size:12px; color:gray;">Example: Lakshya, Jaya, TestUser1</p>
    </div>

    <div class="card">
        <h2>2. Partner A: Code Banao</h2>
        <button onclick="generateCode()">Generate Pairing Code</button>
        <div id="codeResult" class="status"></div>
    </div>

    <div class="card">
        <h2>3. Partner B: Code Daalo</h2>
        <input type="text" id="partnerCode" placeholder="Enter Partner's Code Here">
        <button onclick="joinPartner()">Connect Partner</button>
        <div id="joinResult" class="status"></div>
    </div>

    <div class="card">
        <h2>4. Test Notification</h2>
        <button onclick="sendLove()">💖 Send Love Notification</button>
        <div id="loveResult" class="status"></div>
    </div>

    <script>
        const baseUrl = window.location.origin; // Automatically gets current URL

        async function generateCode() {
            const myId = document.getElementById('myId').value;
            if(!myId) return alert("Pehle apna Naam/ID daalo!");
            
            const res = await fetch(baseUrl + '/api/get-code', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user_id: myId })
            });
            const data = await res.json();
            document.getElementById('codeResult').innerText = data.code ? "Tera Code: " + data.code : "Error: " + data.error;
        }

        async function joinPartner() {
            const myId = document.getElementById('myId').value;
            const code = document.getElementById('partnerCode').value;
            if(!myId || !code) return alert("Naam aur Code dono zaruri hai!");

            const res = await fetch(baseUrl + '/api/pair-users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user_id: myId, code: code })
            });
            const data = await res.json();
            document.getElementById('joinResult').innerText = data.status === 'success' ? "Connected with: " + data.partner_id : "Error: " + data.error;
        }

        async function sendLove() {
            const myId = document.getElementById('myId').value;
            if(!myId) return alert("Naam daalo!");

            const res = await fetch(baseUrl + '/api/send-love', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ sender_id: myId })
            });
            const data = await res.json();
            document.getElementById('loveResult').innerText = data.status === 'success' ? "Notification Bhej Diya! ✅" : "Error: " + data.error;
        }
    </script>
</body>
</html>
"""

@app.route('/test')
def test_page():
    return render_template_string(TEST_UI_HTML)

@app.route('/')
def home():
    return "JustUs Backend is Live! 🚀 Go to /test to use the app."

@app.route('/keep-alive')
def keep_alive():
    return "Awake!", 200

# --- API ROUTES (Wahi purane wale) ---

@app.route('/api/get-code', methods=['POST'])
def get_pairing_code():
    try:
        user_id = request.json.get('user_id')
        if not user_id: return jsonify({"error": "User ID missing"}), 400
        
        code = generate_code()
        db.reference(f'pairing_codes/{code}').set(user_id)
        return jsonify({"status": "success", "code": code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pair-users', methods=['POST'])
def pair_users():
    try:
        user_b_id = request.json.get('user_id')
        input_code = request.json.get('code')

        if not user_b_id or not input_code: return jsonify({"error": "Data missing"}), 400

        code_ref = db.reference(f'pairing_codes/{input_code}')
        user_a_id = code_ref.get()

        if not user_a_id: return jsonify({"error": "Invalid Code"}), 404
        if user_a_id == user_b_id: return jsonify({"error": "Khud se connect nahi ho sakte"}), 400

        # Dono ko link karo
        db.reference(f'users/{user_a_id}/partner').set(user_b_id)
        db.reference(f'users/{user_b_id}/partner').set(user_a_id)

        code_ref.delete()
        return jsonify({"status": "success", "partner_id": user_a_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/send-love', methods=['POST'])
def send_love():
    try:
        sender_id = request.json.get('sender_id')
        user_ref = db.reference(f'users/{sender_id}/partner')
        partner_id = user_ref.get()

        if not partner_id: return jsonify({"error": "Partner nahi mila! Pehle connect karo."}), 400

        # Notification Database mein daalo
        db.reference(f'notifications/{partner_id}').push({
            'title': 'Love Alert! ❤️',
            'body': 'Your partner is thinking of you!',
            'timestamp': {".sv": "timestamp"}
        })
        return jsonify({"status": "success", "message": "Sent!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)