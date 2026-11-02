import time
import json
import paho.mqtt.client as mqtt

# ============================================================
# 10-SECOND CLEARANCE TEST
# ============================================================

BROKER = "localhost"
PORT = 1883
TOPIC = "edge/wildlife/status"

CLEAR_DELAY = 10


print("=" * 60)
print("10-SECOND CLEARANCE TEST")
print("=" * 60)


# ============================================================
# MQTT CONNECTION
# ============================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="clearance_test"
)

print("\nConnecting to MQTT...")

client.connect(
    BROKER,
    PORT,
    60
)

client.loop_start()

print("MQTT connected successfully.")


# ============================================================
# PUBLISH FUNCTION
# ============================================================

def publish(message):

    payload = json.dumps(message)

    print("\nMQTT PUBLISH:")
    print(payload)

    result = client.publish(
        TOPIC,
        payload
    )

    result.wait_for_publish()

    print("MQTT message sent.")


# ============================================================
# STEP 1 — SIMULATE ANIMAL DETECTION
# ============================================================

print("\n----------------------------------------")
print("STEP 1: ANIMAL DETECTED")
print("----------------------------------------")

publish({
    "status": "THREAT",
    "object": "animal",
    "timestamp": int(time.time())
})


# ============================================================
# STEP 2 — SIMULATE ANIMAL LEAVING
# ============================================================

print("\n----------------------------------------")
print("STEP 2: ANIMAL HAS LEFT THE FRAME")
print("----------------------------------------")

print("\nStarting 10-second clearance timer...")

start_time = time.time()


# ============================================================
# 10 SECOND COUNTDOWN
# ============================================================

while True:

    elapsed = time.time() - start_time

    remaining = CLEAR_DELAY - elapsed

    if remaining <= 0:
        break

    print(
        f"\rCLEAR IN: {remaining:.1f} seconds",
        end="",
        flush=True
    )

    time.sleep(0.1)


# ============================================================
# STEP 3 — CLEAR
# ============================================================

print("\n\n----------------------------------------")
print("STEP 3: CLEAR")
print("----------------------------------------")

publish({
    "status": "CLEAR",
    "timestamp": int(time.time())
})


# ============================================================
# CLEANUP
# ============================================================

time.sleep(1)

client.loop_stop()
client.disconnect()

print("\n" + "=" * 60)
print("10-SECOND CLEARANCE TEST FINISHED")
print("=" * 60)