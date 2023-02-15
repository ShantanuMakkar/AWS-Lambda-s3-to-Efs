# AWS-Lambda-s3-to-Efs
AWS Lambda Function to Download the file from s3, extract the file name in the temp directory of Lambda, and copy the file to EFS File System.


1. Lambda Env Variables :

BUCKET_NAME	-  test-bucket
EFS_MOUNT	-   /mnt/efs
TEMP_DIR	-   /tmp

2. Attach EFS File System with Lambda with Local mount path as - /mnt/efs

3. Attach S3 as Trigger to Lambda to invoke the function as and when a file is uploaded to s3

4. Test Function Event in Lambda 

{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-2",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "test-bucket",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::xtb-test-bucket"
        },
        "object": {
          "key": "s3-trigger.txt",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}
