import json
import boto3

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reservaciones')

def lambda_handler(event, context):
    try:
        response = table.scan()
        reservations = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(reservations),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
