import paho.mqtt.client as mqtt
import time
import random

# Setari Broker MQTT (Acum e local, cand il mutam pe AWS, schimbam doar IP-ul aici)
BROKER_IP = "3.75.213.20"  # localhost, pentru ca ruleaza pe laptopul tau in Docker
PORT = 1883
TOPIC_TEMP = "licenta/temperatura"

# Initiem clientul MQTT (aici am adaugat versiunea de API ceruta de noua actualizare)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "ESP32_Virtual_Florin")

print(f"Incercare de conectare la broker-ul {BROKER_IP}:{PORT}...")
client.connect(BROKER_IP, PORT)
print("Conectat cu succes! Incep trimiterea datelor simulate...")

try:
    while True:
        # Simulam o temperatura intre 20.0 si 40.0 grade Celsius
        temp_simulata = round(random.uniform(20.0, 40.0), 1)
        
        # Publicam mesajul catre broker
        client.publish(TOPIC_TEMP, str(temp_simulata))
        print(f"[PUBLISH] Am trimis temperatura: {temp_simulata}°C pe topicul '{TOPIC_TEMP}'")
        
        # Asteptam 2 secunde inainte sa trimitem o noua valoare (exact cum ar face DHT22)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nOprire senzor virtual...")
    client.disconnect()