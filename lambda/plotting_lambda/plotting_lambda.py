import boto3
import matplotlib.pyplot as plt
from boto3.dynamodb.conditions import Key
import time
import io
import os

# 初始化 DynamoDB 和 S3 客户端
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
s3 = boto3.client('s3', region_name='us-west-2')

def lambda_handler(event, context):
    # 从环境变量获取桶和表的名称
    bucket_name = os.getenv('BUCKET_NAME', 'default-bucket-name')  # 使用环境变量传递真实名称
    table_name = os.getenv('TABLE_NAME', 'default-table-name')      # 使用环境变量传递真实名称

    # 确保 bucket_name 和 table_name 已正确配置
    if bucket_name == 'default-bucket-name' or table_name == 'default-table-name':
        print("Warning: Using default bucket or table name. Ensure environment variables are set.")
    
    # 获取 DynamoDB 表引用
    table = dynamodb.Table(table_name)
    current_time = int(time.time())
    start_time = current_time - 2500  # 时间窗口

    try:
        # 查询 DynamoDB 以获取指定时间窗口内的数据
        response = table.query(
            KeyConditionExpression=Key('BucketName').eq(bucket_name) &
                                   Key('Timestamp').between(str(start_time), str(current_time))
        )
        items = response.get('Items', [])
        print(f"DynamoDB query result: {items}")

        # 检查是否有数据返回
        if not items:
            print("No data retrieved from DynamoDB.")
            return {
                'statusCode': 400,
                'body': 'No data to plot.'
            }

        # 准备绘图数据
        timestamps = [int(item['Timestamp']) for item in items]
        sizes = [item['TotalSize'] for item in items]
        max_size = max(sizes)
        
        print(f"Plot data - sizes: {sizes}, timestamps: {timestamps}")

        # 创建绘图
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, sizes, label='Bucket Size', color='blue', linewidth=2, marker='o', markersize=8)
        plt.axhline(y=max_size, color='red', linestyle='--', label='Historical High')
        plt.ylim(0, max_size + 5000)
        plt.xlabel('Timestamp')
        plt.ylabel('Bucket Size (Bytes)')
        plt.title('Bucket Size Over Time')
        plt.xticks(rotation=45)
        plt.legend()

        # 将绘图保存到内存缓冲区
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # 保存绘图到 S3
        print("Saving plot to S3...")
        s3.put_object(Bucket=bucket_name, Key='plot.png', Body=buffer, ContentType='image/png')
        print("Plot saved to S3.")

        return {
            'statusCode': 200,
            'body': 'Plot saved to S3.'
        }

    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f'Error occurred: {e}'
        }