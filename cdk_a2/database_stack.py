from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    CfnOutput
)
from constructs import Construct

class DatabaseStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.table = dynamodb.Table(
            self, "S3ObjectSizeHistory",
            partition_key=dynamodb.Attribute(name="BucketName", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="Timestamp", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        CfnOutput(self, "TableNameOutput", value=self.table.table_name, export_name="TableName")