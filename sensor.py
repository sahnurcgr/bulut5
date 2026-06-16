#"endpointAddress": "a2sjjocoz2jokj-ats.iot.us-east-1.amazonaws.com"
import time
import random
import json
import ssl
import paho.mqtt.client as mqtt

# --- AWS IOT AYARLARI ---
AWS_ENDPOINT = "a2sjjocoz2jokj-ats.iot.us-east-1.amazonaws.com" 
PORT = 8883
CLIENT_ID = "sensor_kizilay_01"
TOPIC = "sehir/cevre/kizilay" # Verilerimizi bu kanaldan (topic) göndereceğiz

# Sertifika dosya isimleri (Uzantılarına ve isimlerine çok dikkat et)
ROOT_CA = "AmazonRootCA1.pem"
CERT_FILE = "086622c9bb4ced451a91245dc5d4a062e95eb82659ffd37ff9ef1c9877ac45a0-certificate.pem.crt" # İndirdiğin crt dosyasının adı
KEY_FILE = "086622c9bb4ced451a91245dc5d4a062e95eb82659ffd37ff9ef1c9877ac45a0-private.pem.key"      # İndirdiğin key dosyasının adı

def generate_sensor_data():
    temperature = round(random.uniform(15.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    co_level = random.randint(10, 80)

    return {
        "sensor_id": CLIENT_ID,
        "timestamp": time.time(),
        "temperature": temperature,
        "humidity": humidity,
        "co_level": co_level
    }

# MQTT İstemcisini (Client) Oluşturma ve Ayarlama
client = mqtt.Client(client_id=CLIENT_ID)

# Güvenlik (TLS/SSL) Ayarları
client.tls_set(ca_certs=ROOT_CA, certfile=CERT_FILE, keyfile=KEY_FILE, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# AWS'ye Bağlanma
print("AWS IoT Core'a bağlanılıyor...")
client.connect(AWS_ENDPOINT, PORT, keepalive=60)
client.loop_start() # Bağlantıyı arka planda açık tutmak için bir thread başlatır
print("Bağlantı başarılı! Veri akışı başlıyor...\n")

if __name__ == "__main__":
    try:
        while True:
            sensor_data = generate_sensor_data()
            payload = json.dumps(sensor_data)
            
            # Veriyi AWS'ye fırlat
            client.publish(TOPIC, payload, qos=1)
            print(f"Gönderildi -> {payload}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSensör durduruldu.")
        client.loop_stop()
        client.disconnect()