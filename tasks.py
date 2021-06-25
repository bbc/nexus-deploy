import os

from cosmic import service, keys
from infrastructure.stacks.service import template

repos = {
    "nexus": {
        "url": "https://repository.api.bbci.co.uk/nexus-el8/revisions/head",
        "type": "mirrorlist",
        "gpg_key": keys.CD_JENKINS,
    },
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
        "InstanceType": "t3a.small",
    },
    dns_subdomain=".".join(reversed(os.getenv("NAME").split("-"))),
    dns_domain="tools.bbc.co.uk.",
)
