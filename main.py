import json
import urllib.parse
import logging
import os
import zipfile
import boto3
from io import BytesIO
from pathlib import Path
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

global dt
global key
global File_PREFIX_DATE
global FILE_NAME

dt = datetime.now()
File_PREFIX_DATE = dt.strftime('%d%m%Y')
FILE_SUFFIX = os.getenv("file_suffix")
FILE_PREFIX = os.getenv("file_prefix")

s3 = boto3.client("s3")

BUCKET_NAME = os.getenv("BUCKET_NAME")
EFS_MOUNT = os.getenv("EFS_MOUNT")
TEMP_DIR = os.getenv("TEMP_DIR")


class c:
    
    #def a(self,event,context):
        
    #    print(" ------------------------------------- ")
    #    print("Starting the File transfer process ..")
    #    global key
    #    print("Extracting the uploaded file name from the s3 Bucket ..")
        
    #    bucket = event['Records'][0]['s3']['bucket']['name']
    #    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    #    response = s3.get_object(Bucket=bucket, Key=key)
        
    #    print("The uploaded File name is: " + key)
    #    print("The uploaded File content type is: " + response['ContentType'])
        
    #    return response['ContentType']
    #    return key
    

    def b(self,context):
        
        key = FILE_PREFIX+File_PREFIX_DATE+FILE_SUFFIX
        print(" ------------------------------------- ")
        print("File name recieved, starting the file download to lambda temp folder ..")
        
        s3_file_path = key
        local_temp_file = f"{TEMP_DIR}/{key}"
        
        s = str({local_temp_file})
        fname = Path(s).resolve().stem
        print("File name without extension :",fname)
        
        local_temp_folder = f"{TEMP_DIR}"
        local_temp_unzip = f"{TEMP_DIR}/{fname}/"
        
        efs_zip_folder = f"{EFS_MOUNT}/zip_files/"
        efs_unzip_folder = f"{EFS_MOUNT}/unzipped_files/"
        
        
        os.makedirs(TEMP_DIR, exist_ok=True)
        with open(local_temp_file, "wb") as f:
            s3.download_fileobj(BUCKET_NAME, s3_file_path, f)
            
        print("Zipped File " + key + " is downloaded to Lambda /tmp folder ..")
        
        with zipfile.ZipFile(local_temp_file, mode='r') as zipf:
            for file in zipf.infolist():
                fileName = file.filename
                print("Contents in the zipped file :",fileName)
        
        print(" ------------------------------------- ")
        print("Extracting all the files from the zip folder ..")        
            
        with zipfile.ZipFile(local_temp_file, mode='r') as zipf:
            zipf.extractall(local_temp_unzip)
            
        print("All Files extracted from the zip folder and stored in the /tmp folder .. ")
        print(os.system(f"ls -la {local_temp_unzip}"))
        
        print(" ------------------------------------- ")
        print("Copying the zip file from /tmp folder to EFS Zip folder ..")
        os.system(f"cp {local_temp_file} {efs_zip_folder}")
        print(os.system(f"ls -la {efs_zip_folder}"))
        
        print("Copying the unzipped files from /tmp folder to EFS Unzip folder ..")
        os.system(f"cp -r {local_temp_unzip} {efs_unzip_folder}")
        print(os.system(f"ls -la {efs_unzip_folder}"))
        
        print(" ------------------------------------- ")
        print("[SUCCESS]", dt, "Files are copied to the EFS File system, Process is complete ..!")
        print(" ------------------------------------- ")
        
    
def lambda_handler(event, context):
    
    x = c()
    #x.a(event,context)
    x.b(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps('EFS File Transfer Function is successful !')
    }
