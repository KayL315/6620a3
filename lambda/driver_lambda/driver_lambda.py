import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['BUCKET_NAME']
    
    # 文件内容和名称
    files = [
        ('assignment1.txt', 'Empty Assignment 1', 19),
        ('assignment2.txt', 'Empty Assignment 2222222222', 28),
        ('assignment3.txt', '33', 2)
    ]
    
    for file_name, content, size in files:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)
        print(f"Uploaded {file_name} with size {size} bytes")
    
    return {
        'statusCode': 200,
        'body': 'Files uploaded successfully.'
    }