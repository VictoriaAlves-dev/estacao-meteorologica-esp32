import time
import threading
import uvicorn
from application.configs.broker_configs import mqtt_broker_configs
from .mqtt_connection.mqtt_client_connection import MqttClientConnection

def start_mqtt():
    print("Iniciando MQTT BROKER........")
    mqtt_client_connection = MqttClientConnection(
            mqtt_broker_configs["HOST"],
            mqtt_broker_configs["PORT"],
            mqtt_broker_configs["CLIENT_NAME"],
            mqtt_broker_configs["KEEPALIVE"],
    )
    mqtt_client_connection.start_connection()
    print("MQTT BROKER iniciado")
        
    while True: time.sleep(0.001)
    

def start():
    thread_mqtt = threading.Thread(target=start_mqtt, daemon=True)
    thread_mqtt.start()
    
    print("Iniciando Uvicorn.......")
    uvicorn.run(
        "application.controller.weather_controller:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )