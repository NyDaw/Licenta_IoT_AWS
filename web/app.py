from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)
ultima_temperatura = "--"

# Setari Broker MQTT
BROKER_IP = "3.75.213.20"
PORT = 1883
TOPIC_TEMP = "licenta/temperatura"

# Functia care se apeleaza automat cand primim un mesaj de la senzor
def on_message(client, userdata, msg):
    global ultima_temperatura
    ultima_temperatura = msg.payload.decode('utf-8')
    print(f"[RECEPTIONAT] Am primit din broker: {ultima_temperatura}°C")

# Functia care tine conexiunea MQTT activa
def pornire_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Flask_Web_App")
    client.on_message = on_message
    client.connect(BROKER_IP, PORT)
    client.subscribe(TOPIC_TEMP)
    client.loop_forever()

# Ruta principala a site-ului
@app.route('/')
def index():
    return render_template('index.html')

# O ruta secreta (API) prin care site-ul va cere temperatura actualizata in fundal
@app.route('/api/temp')
def get_temp():
    return jsonify({'temperatura': ultima_temperatura})

if __name__ == '__main__':
    # Pornim MQTT intr-un proces separat (thread) ca sa nu blocheze incarcarea site-ului
    thread_mqtt = threading.Thread(target=pornire_mqtt)
    thread_mqtt.daemon = True
    thread_mqtt.start()
    
    # Pornim site-ul web pe portul 5000
    app.run(debug=True, port=5000, use_reloader=False)