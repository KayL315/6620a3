from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_sns as sns,
    CfnOutput,
    Duration
)
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        self.bucket = s3.Bucket(self, "TestBucket")

        # Create SQS queue with visibility timeout (at least 900 seconds)
        self.sqs_queue = sqs.Queue(
            self, 
            "MyQueue",
            visibility_timeout=Duration.seconds(900)  # Set to 900 seconds (15 minutes)
        )

        # Create SNS topic
        self.sns_topic = sns.Topic(self, "MyTopic")

        # Create S3 event notification to SNS
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.SnsDestination(self.sns_topic)
        )

        # Output bucket name
        CfnOutput(self, "BucketNameOutput", value=self.bucket.bucket_name, export_name="BucketName")

        # Output SQS queue URL
        CfnOutput(self, "SqsQueueUrl", value=self.sqs_queue.queue_url, export_name="SqsQueueUrl")

        # Output SQS queue ARN
        CfnOutput(self, "SqsQueueArn", value=self.sqs_queue.queue_arn, export_name="SqsQueueArn")