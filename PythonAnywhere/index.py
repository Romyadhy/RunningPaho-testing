import ssl
import time
import requests
import paho.mqtt.client as mqtt

# === CONFIGURATION ===
TELEGRAM_BOT_TOKEN = "7744245206:AAHGAlfLOK3F3ECSpVHSEQJIfxDay4qT5fo"
TELEGRAM_CHAT_ID = "5344109406"

MQTT_BROKER = "your-cluster.s1.eu.hivemq.cloud"
MQTT_PORT = 8884  # WebSocket Secure
MQTT_USERNAME = "Birjon"
MQTT_PASSWORD = "Birjon123"
MQTT_TOPIC = "testing/render"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload)
        if r.status_code != 200:
            print("❌ Telegram Error:", r.text)
    except Exception as e:
        print("❌ Telegram Exception:", e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ via WSS")
        message = "📡 MQTT message from Render background worker!"
        client.publish(MQTT_TOPIC, message)
        print(f"📤 Published: {message}")
        send_telegram(f"✅ MQTT Published: {message}")
    else:
        print("❌ MQTT Connection failed. Code:", rc)
        send_telegram("❌ MQTT Connection Failed.")

def main():
    client = mqtt.Client(transport="websockets")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print("❌ Error:", e)
        send_telegram(f"❌ MQTT Error: {e}")

if __name__ == "__main__":
    main()
