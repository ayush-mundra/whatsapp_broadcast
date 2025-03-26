import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    # Example usage
    phone_number = "6375879100"  # Replace with actual phone number
    name = "John"
    query = "Hello from WhatsApp API"
    
    try:
        result = send_whatsapp(phone_number, name, query)
        print("Message sent successfully:", result)
    except Exception as e:
        print("Error sending message:", str(e))


