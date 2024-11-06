import boto3
import time
import requests
import os

s3_client = boto3.client('s3', region_name='us-west-2')
lambda_client = boto3.client('lambda', region_name='us-west-2')

def lambda_handler(event, context):
    # 从环境变量中获取 bucket 名称和 API URL
    bucket_name = os.getenv('BUCKET_NAME')
    api_url = os.getenv('API_URL')

    if not bucket_name or not api_url:
        print("Error: Missing environment variables BUCKET_NAME or API_URL.")
        return {
            'statusCode': 400,
            'body': 'Missing required environment variables.'
        }

    try:
        print(f"Starting operations on bucket: {bucket_name}")
        
        # 创建对象
        print("Creating 'assignment1.txt'...")
        s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
        time.sleep(5)

        # 更新对象
        print("Updating 'assignment1.txt'...")
        s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
        time.sleep(5)

        # 删除对象
        print("Deleting 'assignment1.txt'...")
        s3_client.delete_object(Bucket=bucket_name, Key='assignment1.txt')
        time.sleep(5)

        # 创建另一个对象
        print("Creating 'assignment2.txt'...")
        s3_client.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')

        # 调用 API
        print("Calling the plotting API...")
        response = requests.post(api_url)
        print(f"API response: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f'Error occurred: {e}'
        }

    return {
        'statusCode': 200,
        'body': 'Operations completed successfully.'
    }