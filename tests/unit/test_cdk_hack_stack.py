import json
import pytest

from aws_cdk import core
from cdk_hack.cdk_hack_stack import CdkHackStack

def get_template():
    app = core.App()
    CdkHackStack(app, "cdk-hack", env=core.Environment(account="987092829714", region="us-west-2"))
    return json.dumps(app.synth().get_stack("cdk-hack").template)

def test_ecs_service():
    assert("Memory" and "512" in get_template())