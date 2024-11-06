from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    CfnOutput
)
from constructs import Construct

class ApiStack(Stack):
    def __init__(self, scope: Construct, id: str, plotting_lambda, **kwargs):
        super().__init__(scope, id, **kwargs)

        api = apigateway.LambdaRestApi(
            self, "PlottingApi",
            handler=plotting_lambda
        )

        plot_resource = api.root.add_resource("plot")
        plot_resource.add_method("GET")

        self.api_url_output = CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="The URL of the API Gateway"
        )