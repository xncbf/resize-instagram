import logging
import boto3
import os

from botocore.exceptions import ClientError
from zappa.asynchronous import task

from resize.settings import AWS_S3_BUCKET_NAME_MEDIA

# @task
def async_upload_file(file_name, bucket=AWS_S3_BUCKET_NAME_MEDIA, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL':'public-read'})
    os.remove(file_name)
    
    # stream byte
    # response = s3_client.put_object( 
    #     Bucket=bucket,
    #     Body=byte_img,
    #     Key=object_name,
    #     ACL='public-read'
    # )
