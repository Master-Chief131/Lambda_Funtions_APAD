import json
import boto3
from datetime import datetime

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reservaciones')

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    # reservation_id = event['pathParameters']['reservationId']
    user_id = event["userId"]
    reservation_id = event["reservationId"]
    
    update_expression = "set details=:d, reservationTime=:rt, reservationType=:rty, updatedAt=:ua"
    expression_attribute_values = {
        ':d': event["details"],
        ':rt': event["reservationTime"],
        ':rty': event["reservationType"],
        ':ua': datetime.utcnow().isoformat()
    }
    
    try:
        response = table.update_item(
            Key={
                'userId': user_id,
                'reservationId': reservation_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Reservation updated'}),
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
