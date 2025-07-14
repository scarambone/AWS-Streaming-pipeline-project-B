import json
import os
import boto3
import requests
from datetime import datetime

kinesis_client = boto3.client('kinesis')
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']
KINESIS_STREAM_NAME = os.environ['KINESIS_STREAM_NAME']

# Lista de cidades
CITIES = ["London", "New York", "Sao Paulo", "Tokyo", "Berlin"]

def lambda_handler(event, context):
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            enriched_data = {
                "city": city,
                "timestamp": datetime.utcnow().isoformat(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "raw": data
            }
            kinesis_client.put_record(
                StreamName=KINESIS_STREAM_NAME,
                Data=json.dumps(enriched_data),
                PartitionKey=city
            )
        else:
            print(f"Erro ao consultar {city}: {response.status_code}")
    
    return {
        "statusCode": 200,
        "body": json.dumps("Consulta e envio para Kinesis concluídos com sucesso.")
    }
