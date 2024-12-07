from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    Duration,
)
from constructs import Construct

class CleanerLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        cleaner_role = iam.Role(self, "CleanerRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )

        self.cleaner_lambda = _lambda.Function(
            self, "CleanerLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="cleaner_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/cleaner_lambda"),
            role=cleaner_role,
            timeout=Duration.minutes(15),
            environment={
                'BUCKET_NAME': bucket_name
            }
        )