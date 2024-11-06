from aws_cdk import (
    Stack,
    aws_s3 as s3,
    CfnOutput
)
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.bucket = s3.Bucket(self, "TestBucket")

        # 输出 bucket 名称供其他堆栈使用
        CfnOutput(self, "BucketNameOutput", value=self.bucket.bucket_name, export_name="BucketName")