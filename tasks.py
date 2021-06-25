import os

from cosmic import service
from infrastructure.stacks.service import template

repos = {
}


namespace = service(
    aws_dev_account="536795411033",
    aws_prod_account="536795411033",
    yum_repos=repos,
    # Happy to have PRs and trunk share Test for cost savings (low PR rate)
    env_branch="test",
    stack=template,
    stack_params={
        "MinSize": "1",
        "MaxSize": "1",
        "DesiredCapacity": "1",
        "UpdateMinInService": "0",
        "InstanceType": "t3.micro",
    },
    dns_subdomain=".".join(reversed(os.getenv("NAME").split("-"))),
    dns_domain="tools.bbc.co.uk.",
)
