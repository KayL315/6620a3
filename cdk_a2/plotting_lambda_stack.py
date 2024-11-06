from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class PlottingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str,table_name: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        plotting_role_arn = "arn:aws:iam::515966507643:role/service-role/plottingLambda-role-s7mtt0nj"
        plotting_role = iam.Role.from_role_arn(
            self, "PlottingRole", role_arn=plotting_role_arn
        )
        numpy_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "NumpyLayer",
            "arn:aws:lambda:us-west-2:770693421928:layer:Klayers-p39-numpy:17"
        )

        matplotlib_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "MatplotlibLayer",
            "arn:aws:lambda:us-west-2:770693421928:layer:Klayers-p39-matplotlib:1"
        )

        self.plotting_lambda = _lambda.Function(
            self, "PlottingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="plotting_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/plotting_lambda"),
            layers=[matplotlib_layer, numpy_layer],
            role=plotting_role,
            timeout=Duration.minutes(15),
            environment={
                'TABLE_NAME': table_name,   # 传递表名
                'BUCKET_NAME': bucket_name   # 传递桶名
            }  
        )