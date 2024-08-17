import os
import json
import boto3
import base64
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table(os.environ['USER_TABLE'])

s3 = boto3.client('s3')
art_bucket = os.environ['ART_BUCKET']

def lambda_handler(event, context):
    try:
        # リクエストのボディをJSONとしてパース
        body = json.loads(event['body'])
        http_method = event['httpMethod']
        
        if http_method == 'POST':
            return handle_post(body)
        else:
            return {
                'statusCode': 405,
                'body': 'Method Not Allowed'
            }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': f"Invalid JSON: {str(e)}"
        }

def handle_post(body):
    try:
        # POSTリクエストのデータを取得
        user_id = body['user_id']
        art_data = body['art_data']  # Base64でエンコードされた画像データ
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # Base64でエンコードされた画像データをデコード
        image_data = base64.b64decode(art_data)

        # S3に画像を保存
        s3_key = f"{user_id}/{timestamp}.png"
        s3.put_object(
            Bucket=art_bucket,
            Key=s3_key,
            Body=image_data,
            ContentType='image/png'
        )

        # DynamoDBにメタデータを保存
        item = {
            'UserId': user_id,
            'Timestamp': timestamp,
            'S3Key': s3_key,
        }
        user_table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image uploaded and metadata saved successfully',
                'item': item,
            }),
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"An error occurred: {e.response['Error']['Message']}"
        }
