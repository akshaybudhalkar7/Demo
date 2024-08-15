from os import path
from aws_cdk import (aws_s3, Stack, aws_lambda, aws_iam, Duration)
from constructs import Construct
import os
from os import path



class DemoStack(Stack):
    def __init__(self, scope: Construct, id:str, environment:None, **kwargs) -> None:
        super().__init__(scope,id,**kwargs)

        sample_bucket = aws_s3.Bucket(
            self,
            "%s-s3" % id,
            bucket_name="%s-s3" % id,
        )

        lambda_exec_role = aws_iam.Role(
            self, 'LambdaRole',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
            ]
        )

        lambda_function = aws_lambda.Function(self,
                                              '%s-lambda' % id,
                                              function_name='%s-lambda' % id,
                                              handler='app.handler',
                                              runtime = aws_lambda.Runtime.PYTHON_3_11,
                                              code= aws_lambda.Code.from_asset(path.join(path.dirname(__file__), '..', '..','application')),
                                              timeout=Duration.minutes(15),
                                              environment = {'DEPLOYMENT_ENV': environment},
                                              role=lambda_exec_role
                                              )

        sample_bucket.grant_read_write(lambda_function)

