# server.py

from flask import Flask, request
import threading
import time
import requests
import json
import os
from dotenv import load_dotenv  # <--- AJOUTER ÇA

load_dotenv()  # <--- CHARGE AUTOMATIQUEMENT TON .env

app = Flask(__name__)

# Configuration (mettre ici tes vraies infos Supabase)
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://xxxxxxxxxxxx.supabase.co"  # Remplace par ton vrai lien
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY") or "your-api-key-here"          # Remplace par ta vraie clé API

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
}

# Fonction qui attend 10 minutes puis supprime le verification_code
def delete_verification_code(email):
    print(f"⏳ Timer started for {email}")
    time.sleep(10 * 60)  # Attend 10 minutes
    url = f"{SUPABASE_URL}/rest/v1/userlogin?email=eq.{email}"
    payload = {
        "verification_code": ""
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    if response.status_code in [200, 204]:
        print(f"✅ Verification code deleted for {email}")
    else:
        print(f"❌ Error deleting code for {email}: {response.status_code} - {response.text}")

# Route API pour démarrer le timer
@app.route('/start_timer', methods=['POST'])
def start_timer():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return {"error": "Email is required"}, 400

    # Lance un nouveau thread pour ne pas bloquer Flask
    threading.Thread(target=delete_verification_code, args=(email,)).start()

    return {"status": f"Timer started for {email}"}, 200

# Point simple pour vérifier que le serveur tourne
@app.route('/', methods=['GET'])
def home():
    return {"message": "GlowUp Clothes Timer Server is running"}, 200

# Démarrage du serveur
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))  # Utiliser PORT imposé par Render si dispo
    app.run(host="0.0.0.0", port=port)