from dotenv import load_dotenv
from db import init_db
from indiamart_api import fetch_leads
from whatsapp_api import send_whatsapp
import time

load_dotenv()
conn = init_db()
cursor = conn.cursor()

def run():
    leads = fetch_leads()

    for lead in leads:
        name = lead.get("SENDER_NAME", "Customer")
        phone = lead.get("MOBILE")
        query = lead.get("QUERY", "your inquiry")

        if not phone:
            continue

        cursor.execute("SELECT * FROM leads WHERE phone = ?", (phone,))
        existing = cursor.fetchone()

        if existing:
            print(f"⏩ Already sent: {phone}")
            continue

        cursor.execute("INSERT INTO leads (name, phone, query) VALUES (?, ?, ?)", (name, phone, query))
        conn.commit()

        try:
            resp = send_whatsapp(phone, name, query)
            if "messages" in resp:
                print(f"✅ Sent to {name} ({phone})")
                cursor.execute("UPDATE leads SET message_sent = 1 WHERE phone = ?", (phone,))
                conn.commit()
            else:
                print(f"❌ Failed for {name} ({phone}):", resp)
        except Exception as e:
            print(f"❌ Exception for {phone}:", str(e))

if __name__ == "__main__":
    while True:
        run()
        print("🔄 Waiting 30 minutes...")
        time.sleep(1800)
