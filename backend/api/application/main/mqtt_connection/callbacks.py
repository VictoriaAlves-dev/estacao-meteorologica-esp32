import json
import pyodbc
from application.configs.pyodbc_configs import GetConnectionString
from application.configs.broker_configs import mqtt_broker_configs

connectionString = GetConnectionString()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"MQTT BROKER | Mosquitto : Client connected {client}")
        client.subscribe(mqtt_broker_configs["TOPIC"])
    else:
        print(f"MQTT BROKER | Mosquitto : Erro ao conectar \nCódigo={rc}")
        
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"MQTT BROKER | Mosquitto : Client subscribed at {mqtt_broker_configs["TOPIC"]}")
    print(f"QOS: {granted_qos}")
    
def on_message(client, userdata, message):
    print(f"MQTT BROKER | Mosquitto : Message received")
    print(client)
    print(message.payload)
    
    topic = message.topic
    measurementValue = str(message.payload.decode("utf-8","ignore"))
    
    SaveToDatabase(topic, measurementValue)
    
def SaveToDatabase(topic, measurementValue):
    try:
        if isinstance(measurementValue, bytes):
            measurementValue = measurementValue.decode("utf-8", "ignore")
        
        measurementValue = str(measurementValue).strip()
        
        dados = json.loads(measurementValue)
        
        temperatura = float(dados.get("temperatura", 0))
        indiceUV = float(dados.get("indice_uv", 0))
        umidade = float(dados.get("umidade", 0))
        
        query = "INSERT INTO TBclima (Temperatura, indiceUV, umidade) VALUES (?,?,?)"
        parameters = (
            temperatura,
            indiceUV,
            umidade
        )
        
        cursor.execute(query, parameters)
        cursor.commit()
        
        print(f"\nMQTT BROKER | Mosquitto : Message registered on Database")
        print(topic + " " + measurementValue)
        
    except Exception as e:
        print(f"Erro ao processar mensagens do MQTT: {e}")