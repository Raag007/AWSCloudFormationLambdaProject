import boto3
def lambda_handler():
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions',[])
    for region in regions:
            reg=region['RegionName']
            ec2 = boto3.client('ec2', region_name=reg)
            result = ec2.describe_volumes( Filters=[{'Name': 'status', 'Values': ['in-use']}])
            for volume in result['Volumes']:
            result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda backup function ebs-snapshots')
            ec2resource = boto3.resource('ec2', region_name=reg)
            snapshot = ec2resource.Snapshot(result['SnapshotId'])
            volumename = 'N/A'
            if 'Tags' in volume:
                for tags in volume['Tags']:
                    if tags["Key"] == 'Name':
                        volumename = tags["Value"]
            snapshot.create_tags(Tags=[{'Key': 'Name','Value': volumename}])
