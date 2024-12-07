import boto3
import matplotlib.pyplot as plt
import io
import time

# 初始化 S3 和 DynamoDB 客户端
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket_name = event['BUCKET_NAME']
    table_name = event['TABLE_NAME']
    
    # 获取 DynamoDB 表
    table = dynamodb.Table(table_name)
    
    # 获取当前时间戳并设置查询时间窗口
    current_time = int(time.time())
    start_time = current_time - 3600  # 查询过去一小时的数据

    # 从 DynamoDB 查询数据
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Timestamp').between(str(start_time), str(current_time)),
        ProjectionExpression="BucketName, Timestamp, TotalSize"
    )
    
    items = response.get('Items', [])
    
    if not items:
        return {
            'statusCode': 400,
            'body': 'No data found for the specified time window.'
        }

    # 准备数据
    timestamps = [item['Timestamp'] for item in items]
    sizes = [item['TotalSize'] for item in items]

    # 创建图表
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, sizes, label='Bucket Size', color='blue')
    plt.title(f"Bucket Size Over Time ({bucket_name})")
    plt.xlabel('Timestamp')
    plt.ylabel('Bucket Size (Bytes)')
    plt.xticks(rotation=45)
    plt.legend()

    # 将图表保存到内存缓冲区
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 将图表上传到 S3
    s3.put_object(Bucket=bucket_name, Key='plot.png', Body=buffer, ContentType='image/png')

    return {
        'statusCode': 200,
        'body': 'Plot saved to S3 successfully.'
    }