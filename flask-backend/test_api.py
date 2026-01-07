import requests

# 🔴 YAHAN APNA RENDER URL PASTE KAR (Last me /api/invite zarur lagana)
url = 'https://justus-exvn.onrender.com//api/invite' 

payload = {
    "sender": "Lakshya_Live_Test",
    "receiver": "Jaya_Live_Test"
}

print("Sending Invite to Render Server... 🚀")

try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Server ne jawab diya.")
        print("Response:", response.json())
    else:
        print("\n❌ FAILED! Server ne mana kar diya.")
        print("Error:", response.text)

except Exception as e:
    print("\n❌ Error:", e)