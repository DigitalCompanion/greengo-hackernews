#!/usr/bin/env python3

from aws_cdk import core

from cdk_hack.cdk_hack_stack import CdkHackStack


app = core.App()
CdkHackStack(app, "cdk-hack")

app.synth()
