from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    Fn,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications
)
from constructs import Construct

class SizeTrackingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, table_name: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        size_tracking_role_arn = "arn:aws:iam::515966507643:role/service-role/sizeTrackingLambda-role-lz328yyo"
        # Import the existing role
        size_tracking_role = iam.Role.from_role_arn(self, "SizeTrackingRole", role_arn=size_tracking_role_arn,mutable=False)
        # size_tracking_role = iam.Role(
        #     self, "SizeTrackingRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        #     managed_policies=[
        #         iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
        #         iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
        #     ]
        # )

        self.size_tracking_lambda = _lambda.Function(
            self, "SizeTrackingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="size_tracking_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/size_tracking_lambda"),
            role=size_tracking_role,
            timeout=Duration.minutes(15),
            environment={
                'BUCKET_NAME': bucket_name,
                'TABLE_NAME': table_name
            }
        )
        bucket = s3.Bucket.from_bucket_name(self, "ImportedBucket", bucket_name)
        # 添加 Lambda 事件通知
        notification = s3_notifications.LambdaDestination(self.size_tracking_lambda)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)
        bucket.add_event_notification(s3.EventType.OBJECT_REMOVED, notification)