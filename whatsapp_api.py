import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify  # Import Flask and necessary modules

load_dotenv()

app = Flask(__name__)  # Create a Flask application

def send_whatsapp(phone, name, query):
    url = "https://graph.facebook.com/v22.0/107095272246745/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('WA_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": f"91{phone}",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": { "code": "en_US" }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/send', methods=['POST'])  # Define a route for sending messages
def send_message():
    data = request.json  # Get JSON data from the request
    phone = data.get('phone')
    name = data.get('name')
    query = data.get('query')

    try:
        result = send_whatsapp(phone, name, query)
        return jsonify({"message": "Message sent successfully", "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway's dynamic PORT or default to 5000
    app.run(debug=True, host="0.0.0.0", port=port)  # Run the Flask app