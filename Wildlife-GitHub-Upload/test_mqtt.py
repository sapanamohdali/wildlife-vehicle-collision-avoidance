import paho.mqtt.client as mqtt
import time
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "edge/wildlife/status"

print("=" * 50)
print("MQTT CONNECTION TEST")
print("=" * 50)

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="wildlife_test"
)

print("\nConnecting to MQTT broker...")

client.connect(BROKER, PORT, 60)

client.loop_start()

time.sleep(1)

message = {
    "status": "THREAT",
    "object": "animal",
    "timestamp": int(time.time())
}

payload = json.dumps(message)

print("\nPublishing:")
print(payload)

result = client.publish(TOPIC, payload)

result.wait_for_publish()

print("\nMessage published successfully.")
print("Topic:", TOPIC)

time.sleep(1)

client.loop_stop()
client.disconnect()

print("\nMQTT TEST FINISHED")