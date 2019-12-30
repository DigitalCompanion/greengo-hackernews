import os
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
    aws_certificatemanager as certmgr,
    aws_route53 as route53,
)


class CdkHackStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=3
        )

        cluster = ecs.Cluster(
            self, "Cluster",
            vpc=vpc
        )

        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="greengocloud.com",
            private_zone=False
        )

        certificate = certmgr.DnsValidatedCertificate(
            self, "HackCertificate",
            domain_name="hackernews.greengocloud.com",
            hosted_zone=hosted_zone
        )

        app = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'Webservice',
            cluster=cluster,
            domain_name="hackernews.greengocloud.com",
            domain_zone=hosted_zone,
            certificate=certificate,
            assign_public_ip=True,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(
                    os.path.join(os.path.dirname(__file__), 'webapp')
                ),
                container_port=8080,
            )
        )
