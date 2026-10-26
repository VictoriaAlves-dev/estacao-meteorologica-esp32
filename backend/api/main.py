import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gmqtt import Client as MQTTClient
import uvicorn

app = FastAPI(title="API Estação Meteorológica", version="1.0")

# Configuração de CORS para permitir a comunicação com o Front-End
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados com Pydantic para validação
class SensorData(BaseModel):
    temperatura: float
    umidade: float
    uv: float

# Armazenamento temporário dos dados recebidos do broker
latest_data = {
    "temperatura": 0.0,
    "umidade": 0.0,
    "uv": 0.0
}

# Parâmetros de ligação MQTT locais
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "estacao/dados"

def on_connect(client, flags, rc, properties):
    print(f"Conectado ao Broker MQTT com código: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, topic, payload, qos, properties):
    global latest_data
    try:
        data = json.loads(payload.decode())
        latest_data.update(data)
        print(f"Dados atualizados: {latest_data}")
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

async def start_mqtt():
    client = MQTTClient("fastapi_backend_client")
    client.on_connect = on_connect
    client.on_message = on_message
    await client.connect(MQTT_BROKER, MQTT_PORT)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_mqtt())

# Endpoint GET para fornecer os dados ao Front-End (Etapa 3)
@app.get("/api/dados", response_model=SensorData)
def get_dados():
    return latest_data

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
