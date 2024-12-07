import json
import logging

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    for record in event['Records']:
        s3_event = json.loads(record['body'])
        object_name = s3_event['object_name']
        size_delta = s3_event['size_delta']
        
        logger.info(f"{{'object_name': '{object_name}', 'size_delta': {size_delta}}}")
    
    return {
        'statusCode': 200,
        'body': 'Logged S3 event data.'
    }