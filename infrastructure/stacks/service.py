from cosmic.stacks import InternalWebServiceTemplate
from cosmosTroposphere.component.coreimports import CoreImports
from troposphere import Join, Ref, Tags, Sub
from troposphere.efs import FileSystem, MountTarget
from troposphere.ec2 import SecurityGroup, SecurityGroupRule
from troposphere.cloudformation import Init, InitConfig, InitFiles, InitFile
from troposphere.autoscaling import Metadata
from troposphere.elasticloadbalancingv2 import Listener, TargetGroup, Action


def template(project_name, component_name):
    """
    Makes a Troposphere template for main service stack on which the Nexus
    service will run.
    """

    # Start with the Cosmos defaults
    template = InternalWebServiceTemplate(
        description="Infrastructure for the {} service".format(component_name),
        project_name=project_name,
        component_name=component_name,
        alarm_actions=False,
    )

    auto_scaling_group = template.resources["ComponentAutoScalingGroup"]
    auto_scaling_group.AvailabilityZones = ["eu-west-1c"]
    auto_scaling_group.VPCZoneIdentifier = [CoreImports.private_subnets()[2]]

    efs_file_system = FileSystem(
        title="NexusFileSystem",
        FileSystemTags=Tags(
            Name=Join("", [Ref("Environment"), "NexusFileSystem"])
        ),
    )
    template.add_resource(efs_file_system)

    efs_security_group = SecurityGroup(
        "FileSystemSecurityGroup",
        SecurityGroupIngress=[
            SecurityGroupRule(
                title="FileSystemSecurityGroupRule",
                IpProtocol="TCP",
                FromPort="2049",
                ToPort="2049",
                SourceSecurityGroupId=Ref("ComponentSecurityGroup"),
            )
        ],
        VpcId=CoreImports.VPC_ID,
        GroupDescription="Allow NFS over TCP",
    )
    template.add_resource(efs_security_group)

    efs_mount_target = MountTarget(
        title="NexusMountTarget",
        FileSystemId=Ref(efs_file_system),
        SecurityGroups=[Ref(efs_security_group)],
        SubnetId=CoreImports.public_subnets()[1],
    )
    template.add_resource(efs_mount_target)

    launch_config = template.resources["ComponentLaunchTemplate"]
    launch_config.Metadata = Metadata(
        Init(
            {
                "config": InitConfig(
                    files=InitFiles(
                        {
                            "/etc/sysconfig/efsinit": InitFile(
                                owner="root",
                                group="root",
                                mode="000444",
                                content=Sub(
                                    "DATA_MOUNT_POINT=${NexusFileSystem}.efs.eu-west-1.amazonaws.com:/\n"
                                ),
                            )
                        }
                    )
                )
            }
        )
    )

    return template
