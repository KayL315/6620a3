from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class PlottingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, table_name: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 设置权限
        plotting_role_arn = "arn:aws:iam::515966507643:role/service-role/plottingLambda-role-s7mtt0nj"
        plotting_role = iam.Role.from_role_arn(
            self, "PlottingRole", role_arn=plotting_role_arn
        )
        
        # 创建 Plotting Lambda
        self.plotting_lambda = _lambda.Function(
            self, "PlottingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="plotting_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/plotting_lambda"),
            layers=[],
            role=plotting_role,
            timeout=Duration.minutes(15),
            environment={
                'TABLE_NAME': table_name,   # 传递表名
                'BUCKET_NAME': bucket_name   # 传递桶名
            }  
        )