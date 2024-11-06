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

        driver_role_arn = "arn:aws:iam::515966507643:role/service-role/driverLambda-role-qlihfadf"
        driver_role = iam.Role.from_role_arn(
            self, "DriverRole", role_arn=driver_role_arn
        )
        requests_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "RequestsLayer",
            "arn:aws:lambda:us-west-2:770693421928:layer:Klayers-p39-requests:19"
        )
        self.driver_lambda = _lambda.Function(
            self, "DriverLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="driver_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/driver_lambda"),
            role=driver_role,
            layers=[requests_layer],
            timeout=Duration.minutes(15),
            environment={
                'BUCKET_NAME': bucket_name,
                'API_URL': api_url
            }
        )