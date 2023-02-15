# AWS-Lambda-s3-to-Efs
AWS Lambda Function to Download the file from s3, extract the file name in the temp directory of Lambda, and copy the file to EFS File System.


1. Lambda Env Variables :

BUCKET_NAME	- xtb-test-bucket
EFS_MOUNT	-   /mnt/efs
TEMP_DIR	-   /tmp

2. Attach EFS File System with Lambda with Local mount path as - /mnt/efs

3. Attach S3 as Trigger to Lambda to invoke the function as and when a file is uploaded to s3
