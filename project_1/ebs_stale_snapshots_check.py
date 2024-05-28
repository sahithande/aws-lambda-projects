import boto3

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')

    # Get all the EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active EC2 instance id's
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Iterate through each snapshot and delete if it's not attached to any volume, or if the volume is not attached to any running ec2 instance
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume.")
        else:
            try:
                # Check if the volume still exists
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    # Delete the volume if it's not attached to any ec2 instance
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted the EBS snapshot {snapshot_id} as it was taken from a volume that was not attached to any running ec2 instances.")
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    # The volume associated with the ec2 instance was not found, it might have been deleted. 
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted the EBS snapshot {snapshot_id}, as it's associated volume was not found.")