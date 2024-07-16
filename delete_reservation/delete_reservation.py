import json
import boto3

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reservaciones')

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    # reservation_id = event['pathParameters']['reservationId']
    user_id = event["userId"]
    reservation_id = event["reservationId"]

    try:
        response = table.delete_item(
            Key={
                'userId': user_id,
                'reservationId': reservation_id
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Reservation deleted'}),
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
