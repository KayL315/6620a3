import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['BUCKET_NAME']

    # 获取桶中的文件列表
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    # 找到最大的文件
    largest_object = max(response.get('Contents', []), key=lambda x: x['Size'])
    
    # 删除最大的文件
    s3.delete_object(Bucket=bucket_name, Key=largest_object['Key'])
    
    return {
        'statusCode': 200,
        'body': f"Deleted largest object: {largest_object['Key']}"
    }