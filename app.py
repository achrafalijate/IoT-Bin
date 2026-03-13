from flask import Flask, request, jsonify
import requests
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/<username>/<model>"
headers = {"Authorization": f"Bearer <TA_CLE_API>"}

MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "iot/detections"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"].read()
    response = requests.post(API_URL, headers=headers, data=image)
    result = response.json()
    client.publish(MQTT_TOPIC, json.dumps(result))
    return jsonify(result)

@app.route("/")
def home():
    return "API Render OK"
