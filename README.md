# aws-lambda-projects

project_1 description:  The Lambda function fetches all EBS snapshots owned by the same account ('self') and also retrieves a list of active EC2 instances (running and stopped). For each snapshot, it checks if the associated volume (if exists) is not associated with any active instance. If it finds a stale snapshot, it deletes it, effectively optimizing storage costs.

project_2 description: Developed a Python script triggered by AWS Config to verify if AWS CloudTrail monitoring is enabled, ensuring compliance with security policies. The script, executed by AWS Lambda, uses Boto3 to interact with AWS services and is automatically triggered by AWS CloudWatch Events based on specific AWS Config rules.




