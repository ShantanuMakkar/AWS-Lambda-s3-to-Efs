import json
import urllib.parse
import logging
import os
import zipfile
import boto3
from io import BytesIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

#Defining Variables
BUCKET_NAME = os.getenv("BUCKET_NAME")
EFS_MOUNT = os.getenv("EFS_MOUNT")
TEMP_DIR = os.getenv("TEMP_DIR")


class c:
    
    def a(self,event,context):
        
        print("Starting the File transfer process ..")
        global key
        print("Extracting the uploaded file name from the s3 Bucket ..")
        
        #Extract Bucket and Object Name
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        response = s3.get_object(Bucket=bucket, Key=key)
        
        print("The uploaded File name is: " + key)
        print("The uploaded File content type is: " + response['ContentType'])
        
        return response['ContentType']
        return key
    

    def b(self,context):
        
        print("File name recieved, starting the file download to lambda temp folder ..")
        
        #Defining Variables
        s3_file_path = key
        local_temp_file = f"{TEMP_DIR}/{key}"
        efs_file_path = f"{EFS_MOUNT}/{key}"
        
        #Downloading file to Lambda /tmp folder
        os.makedirs(TEMP_DIR, exist_ok=True)
        with open(local_temp_file, "wb") as f:
            s3.download_fileobj(BUCKET_NAME, s3_file_path, f)
            
        print("File " + key + " is downloaded to Lambda /tmp folder ..")
        print("Copying file from /tmp folder to EFS File System ..")
    
        #File transfer from Lambda /tmp to EFS File System        
        os.system(f"cp {local_temp_file} {efs_file_path}")
        print("File is copied to the EFS File system ..")
        
        print(os.system(f"ls -la {EFS_MOUNT}"))

        return {"statusCode": 200}  
        
    
def lambda_handler(event, context):
    
    x = c()
    x.a(event,context)
    x.b(event)
