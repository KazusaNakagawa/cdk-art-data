from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct

class CdkArtDataStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for storing art resources
        art_resources_bucket = s3.Bucket(
            self, "ArtResourcesBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create DynamoDB table for storing user data
        user_data_table = dynamodb.Table(
            self, "UserDataTable",
            partition_key=dynamodb.Attribute(
                name="UserId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="Timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )


        # Create a Lambda function for handling API requests
        handler_lambda = _lambda.Function(
            self, "HandlerLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "USER_TABLE": user_data_table.table_name,
                "ART_BUCKET": art_resources_bucket.bucket_name,
            }
        )

        # Grant the Lambda function read/write permissions to the DynamoDB table
        # user_data_table.grant_read_write_data(handler_lambda)
        user_data_table.grant_full_access(handler_lambda)

        # Grant the Lambda function read/write permissions to the S3 bucket
        art_resources_bucket.grant_read_write(handler_lambda)

        # Create an API Gateway REST API
        api = apigateway.RestApi(
            self, "ArtEducationAPI",
            rest_api_name="Art Education Service"
        )

        # Create an API Gateway integration with the Lambda function
        api_integration = apigateway.LambdaIntegration(handler_lambda)

        # Define a resource and method for the API
        api.root.add_method("POST", api_integration)

        # Optionally, create permissions for Amazon Lex and other services# (This part of the code can be extended based on specific needs)# Create IAM Role for Lex with Lambda permissions
        lex_role = iam.Role(
            self, "LexRole",
            assumed_by=iam.ServicePrincipal("lex.amazonaws.com"),
        )
        lex_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole")
        )

        # Additional resources like Amazon Lex, Polly, Rekognition, etc.# can be added similarly based on the detailed requirements.
