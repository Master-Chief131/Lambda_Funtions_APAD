import json
import boto3
import uuid
from datetime import datetime

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reservaciones')

def lambda_handler(event, context):
    
    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    
    user_id=str(uuid.uuid4())
    
    details = event["details"]
    reservationTime = event["reservationTime"]
    reservationType = event["reservationType"]
    # Generar un ID único para la reserva y el timestamp
    reservation_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    # Crear el ítem para guardar en DynamoDB
    item = {
        'userId': user_id,
        'reservationId': reservation_id,
        'timestamp': timestamp,
        'details': details,
        'status': 'pending',
        'reservationTime': reservationTime,
        'reservationType': reservationType
    }

    try:
        # Guardar el ítem en la tabla DynamoDB
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps({'reservationId': reservation_id}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        # Manejo de errores
        print("Error: ", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
