#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_art_data.cdk_art_data_stack import CdkArtDataStack


app = cdk.App()
CdkArtDataStack(app, 'CdkArtDataStack',
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()
