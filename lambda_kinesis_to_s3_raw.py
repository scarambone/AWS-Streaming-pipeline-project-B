import boto3
import json
import gzip
import base64
import os
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    records = []
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        json_payload = json.loads(payload)
        records.append(json_payload)
    
    # Gera nome de arquivo com timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
    file_key = f"raw/weather_data_{timestamp}.json"
    
    # Salva no S3
    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(records, indent=2)
    )
    
    return {
        'statusCode': 200,
        'body': f'Saved {len(records)} records to {file_key}'
    }
