import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client("estacao_publisher")
mqtt_client.connect(host="localhost", port=1883)
mqtt_client.publish(topic="estacao/dados", payload='{"temperatura":30.3,"umidade":40,"indice_uv":3}')
mqtt_client.publish(topic="estacao/dados", payload='{"temperatura":32,"umidade":40,"indice_uv":3}')
mqtt_client.publish(topic="estacao/dados", payload='{"temperatura":30,"umidade":50,"indice_uv":2}')
mqtt_client.publish(topic="estacao/dados", payload='{"temperatura":17,"umidade":50,"indice_uv":2}')
mqtt_client.publish(topic="estacao/dados", payload='{"temperatura":26.4,"umidade":60,"indice_uv":1}')