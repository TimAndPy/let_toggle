import Jetson.GPIO as GPIO
import paho.mqtt.client as mqtt
import asyncio
import websockets
import json
import time

# GPIO setup
RELAY_PIN = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)

# MQTT instellingen
MQTT_BROKER = "broker.hivemq.com"  # Gebruik een publieke broker of je eigen (bijv. Mosquitto)
MQTT_PORT = 1883
MQTT_TOPIC = "jetson/relay/control"
MQTT_CLIENT_ID = "jetson_nano_client"

# WebSocket instellingen
WEBSOCKET_PORT = 8765
connected_clients = set()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Verbonden met MQTT broker met code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Geabonneerd op topic {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Bericht ontvangen op {msg.topic}: {payload}")
        if payload == "ON":
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            status = {"relay": "ON"}
            print("Relay AAN")
        elif payload == "OFF":
            GPIO.output(RELAY_PIN, GPIO.LOW)
            status = {"relay": "OFF"}
            print("Relay UIT")
        else:
            print("Ongeldig commando")
            return
        # Stuur status naar WebSocket-clients
        asyncio.run(notify_clients(status))
    except Exception as e:
        print(f"Fout bij verwerken bericht: {e}")

# WebSocket server
async def handle_websocket(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"WebSocket bericht ontvangen: {data}")
            # Optioneel: verwerk WebSocket-berichten (bijv. directe relay-besturing)
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket verbinding gesloten")
    finally:
        connected_clients.remove(websocket)

async def notify_clients(status):
    if connected_clients:
        message = json.dumps(status)
        await asyncio.gather(*(client.send(message) for client in connected_clients))

# Start MQTT client
mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Start WebSocket server
async def main():
    try:
        websocket_server = await websockets.serve(handle_websocket, "0.0.0.0", WEBSOCKET_PORT)
        print(f"WebSocket server draait op ws://0.0.0.0:{WEBSOCKET_PORT}")
        await websocket_server.wait_closed()
    except Exception as e:
        print(f"Fout in WebSocket server: {e}")
    finally:
        GPIO.cleanup()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

# Voer de WebSocket server uit
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programma gestopt door gebruiker")
    finally:
        GPIO.cleanup()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()