import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    table_name = event['TABLE_NAME']
    
    # 解析 SQS 消息
    for record in event['Records']:
        s3_event = json.loads(record['body'])
        bucket_name = s3_event['bucket_name']
        object_key = s3_event['object_key']
        size = s3_event['size']

        # 存储文件信息到 DynamoDB
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'BucketName': {'S': bucket_name},
                'ObjectKey': {'S': object_key},
                'Size': {'N': str(size)}
            }
        )
    
    return {
        'statusCode': 200,
        'body': 'Size information saved to DynamoDB.'
    }