import json
import boto3
from botocore.exceptions import ClientError
from common import env, log


S3_BUCKET = env.get_key('S3_BUCKET_NAME')
S3_FOLDER = env.get_key('S3_FOLDER')

def _full_key(file_name):
    return "{0}/{1}".format(S3_FOLDER, file_name).replace('//','/')


def upload_file(dest_key, source_path):

    dest_key = _full_key(dest_key)
    # Upload the file
    s3_client = boto3.client('s3')

    log.info("uploading data to s3 bucket")
    response = s3_client.upload_file(Filename=source_path, Bucket=S3_BUCKET, Key=dest_key)


def download_file(src_file_name, dest_file_name):
    src_file_name = _full_key(src_file_name)
    s3_client = boto3.client('s3')
    try:
        log.info("downloading data from s3 bucket")
        s3_client.download_file(Bucket=S3_BUCKET, Key=src_file_name, Filename=dest_file_name)

    except ClientError as e:
        log.error(e)
        log.info("downloading failed. key:{0}".format(src_file_name))
        
def file_exists(file_name):
    s3_client = boto3.client('s3')
    file_name = _full_key(file_name)
    try:
        log.info("checking key in s3 bucket")
        s3_client.head_object(Bucket=S3_BUCKET, Key=file_name)

        return True
    except ClientError as e:
        log.error(e)
        log.info("key check failed. key:{0}".format(file_name))
        
    return False