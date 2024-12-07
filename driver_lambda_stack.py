from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class DriverLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, bucket_name: str, api_url: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        driver_role = iam.Role(self, "DriverRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )

        # Create Driver Lambda
        self.driver_lambda = _lambda.Function(
            self, "DriverLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="driver_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/driver_lambda"),
            role=driver_role,
            timeout=Duration.minutes(15),
            environment={
                'BUCKET_NAME': bucket_name,
                'API_URL': api_url  # Make sure api_url is passed here
            }
        )