from flask import Flask, request, jsonify
import time
import threading
import requests
import os

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

@app.route('/start_timer', methods=['POST'])
def start_timer():
    data = request.get_json()
    email = data.get('email')
    if email:
        print(f"⏳ Timer started for {email}")
        threading.Thread(target=delete_verification_code, args=(email,)).start()
        return jsonify({"message": "Timer started"}), 200
    else:
        return jsonify({"error": "No email provided"}), 400

def delete_verification_code(email):
    time.sleep(600)  # 10 minutes en secondes
    print(f"🧹 Deleting verification code for {email}")

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    url = f"{SUPABASE_URL}/rest/v1/userlogin?email=eq.{email}"
    payload = {"verification_code": ""}
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 204:
        print(f"✅ Verification code deleted for {email}")
    else:
        print(f"❌ Failed to delete verification code for {email}: {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 3000))
