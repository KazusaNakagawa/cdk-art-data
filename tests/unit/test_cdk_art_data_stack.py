import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_art_data.cdk_art_data_stack import CdkArtDataStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_art_data/cdk_art_data_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkArtDataStack(app, "cdk-art-data")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
