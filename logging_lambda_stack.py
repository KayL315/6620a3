from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_iam as iam,
    Duration
)
from aws_cdk import aws_lambda_event_sources as _lambda_event_sources  # 确保导入这个模块
from constructs import Construct

class LoggingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, sqs_queue: sqs.Queue, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 定义 logging lambda 的角色
        logging_lambda_role = iam.Role(
            self, "LoggingLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")
            ]
        )

        # 创建 Logging Lambda
        self.logging_lambda = _lambda.Function(
            self, "LoggingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="logging_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/logging_lambda"),
            role=logging_lambda_role,
            timeout=Duration.minutes(15),
            environment={
                'SQS_QUEUE_URL': sqs_queue.queue_url
            }
        )

        # 创建 SQS 事件源
        self.logging_lambda.add_event_source(
            _lambda_event_sources.SqsEventSource(sqs_queue)  # 添加 SQS 作为 Lambda 的事件源
        )