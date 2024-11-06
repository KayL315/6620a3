import boto3
import time
import os
import logging

# 初始化日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def lambda_handler(event, context):
    # 从环境变量中获取 bucket 和表的名称
    bucket_name = os.environ.get('BUCKET_NAME', 'default-bucket-name')
    table_name = os.environ.get('TABLE_NAME', 'default-table-name')
    
    logger.info("Lambda function triggered.")
    logger.info(f"Event received: {event}")
    
    # 获取 S3 存储桶的内容
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    total_size = 0
    total_objects = 0
    
    if 'Contents' in response:
        for obj in response['Contents']:
            total_size += obj['Size']
            total_objects += 1
            logger.info(f"Object: {obj['Key']}, Size: {obj['Size']} bytes")
    
    logger.info(f"Total size of bucket {bucket_name}: {total_size} bytes")
    logger.info(f"Total number of objects in bucket {bucket_name}: {total_objects}")
    
    timestamp = str(int(time.time()))
    
    table = dynamodb.Table(table_name)
    try:
        table.put_item(
            Item={
                'BucketName': bucket_name,
                'Timestamp': timestamp,
                'TotalSize': total_size,
                'ObjectCount': total_objects,
                'RecordedAt': timestamp
            }
        )
        logger.info(f"Data written to DynamoDB with timestamp {timestamp}")
    except Exception as e:
        logger.error(f"Error writing to DynamoDB: {e}")
    
    return {
        'statusCode': 200,
        'body': 'Bucket size recorded successfully.'
    }