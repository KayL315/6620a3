from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sqs as sqs,
    Duration
)
from aws_cdk import aws_lambda_event_sources as _lambda_event_sources
from constructs import Construct
from aws_cdk import Fn

class SizeTrackingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, table_name: str, bucket_name: str, sqs_queue_url: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Import the existing IAM role
        size_tracking_role_arn = "arn:aws:iam::515966507643:role/service-role/sizeTrackingLambda-role-lz328yyo"
        size_tracking_role = iam.Role.from_role_arn(self, "SizeTrackingRole", role_arn=size_tracking_role_arn, mutable=False)

        # Add permission for Lambda to receive messages from the SQS queue
        sqs_queue = sqs.Queue.from_queue_attributes(
            self, "ImportedSQSQueue",
            queue_url=sqs_queue_url,  # Using the imported queue URL
            queue_arn=Fn.import_value("SqsQueueArn")  # Using the imported queue ARN
        )

        sqs_queue.grant_consume_messages(size_tracking_role)  # Grant permission to Lambda

        # Lambda function to consume SQS messages
        self.size_tracking_lambda = _lambda.Function(
            self, "SizeTrackingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="size_tracking_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/size_tracking_lambda"),
            role=size_tracking_role,
            timeout=Duration.minutes(15),
            environment={
                'BUCKET_NAME': bucket_name,
                'TABLE_NAME': table_name,
                'SQS_QUEUE_URL': sqs_queue_url  # Passing the queue URL as an environment variable
            }
        )

        # Add SQS as a trigger for the Lambda function
        self.size_tracking_lambda.add_event_source(
            _lambda_event_sources.SqsEventSource(sqs_queue)
        )