import boto3
import json

def lambda_handler(event, context):
    # Get the specified EC2 instance
    ec2_client = boto3.client('ec2')

    # Assume compliant by default
    compliance_status = "COMPLIANT"

    # Extract the configuration item from the invokingEvent
    config = json.loads(event['invokingEvent'])

    configuration_item = config['configurationItem']
    
    # Extract the instance id
    instance_id = configuration_item['configuration']['instanceId']

    # Get complete instance details
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]

    # Check if the specific EC2 Instance has cloudtrail logging enabled
    if not instance['Monitoring']['State'] == "enabled":
        compliance_status = "NON_COMPLIANT"

    evaluation = {
        'ComplianceResourceType': 'AWS::EC2::Instance',
        'ComplianceResourceId': instance_id,
        'ComplianceType': compliance_status,
        'Annotation': 'Detailed monitoring is not enabled.',
        'OrderingTimestamp': config['notificationCreationTime']
    }

    config_client = boto3.client('config')

    response = config_client.put_evaluations(
        Evaluations=[evaluation],
        ResultToken=event['resultToken']
    )

    return response