@Library('cd-pipelines') _
import cdpipelines.LaunchPolicy

def accountId

node {
    env.NAME = env.JOB_NAME.split('/')[0]
    env.VERSION = '0.0.0'

    accountId = sh (
        script: 'curl http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .accountId',
        returnStdout: true
    ).trim()
}

cosmosServicePipeline {
    awsAccounts = [
        dev: accountId,
        prod: accountId,
    ]
    launchPolicy = LaunchPolicy.NEVER_REQUIRE_APPROVAL
    testJobs = []
}
