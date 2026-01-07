import os
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# --- FIREBASE CONNECTION SETUP ---
# Ye logic check karega: Laptop pe hai ya Render pe?
firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')

if firebase_creds:
    # Agar Render pe hain, toh environment variable se key uthayenge
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
else:
    # Agar Laptop pe hain, toh file se key uthayenge
    # Note: Make sure 'serviceAccountKey.json' isi folder mein ho
    cred = credentials.Certificate("serviceAccountKey.json")

# Firebase initialize karna
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://justus-bd376-default-rtdb.firebaseio.com/' 
        # Note: Maine screenshot se tera Project ID 'justus-bd376' dekh liya tha, 
        # agar URL alag ho toh Firebase Console se check kar lena.
    })

# --- ROUTES (Raste) ---

@app.route('/')
def home():
    return "JustUs Backend is Live! 🚀"

@app.route('/keep-alive')
def keep_alive():
    return "I am awake!", 200

# Ye endpoint Flutter call karega invite bhejne ke liye
@app.route('/api/invite', methods=['POST'])
def send_invite():
    try:
        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')

        if not sender or not receiver:
            return jsonify({"error": "Sender aur Receiver ID zaruri hai"}), 400

        # Database mein notification daalna
        ref = db.reference(f'notifications/{receiver}')
        ref.push({
            'title': 'Game Invite',
            'body': f'{sender} wants to play!',
            'timestamp': {".sv": "timestamp"}
        })
        
        return jsonify({"status": "success", "message": "Invite Sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)