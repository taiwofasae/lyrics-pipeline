import argparse
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 upload script")

    subparsers = parser.add_subparsers(title="action", dest="command")

    # Function 1 subparser
    upload_func = subparsers.add_parser("upload", help="Upload")
    upload_func.add_argument("--dest_key", '-d', required=True, help="Destination key")
    upload_func.add_argument("--source_path", '-s', required=True, help="path of source")

    # Function 2 subparser
    download_func = subparsers.add_parser("download", help="Download")
    download_func.add_argument("--src_file_name", '-s', required=True, help="Source file path")
    download_func.add_argument("--dest_file_name", '-d', required=True, help="path of destination")
    
    file_exists = subparsers.add_parser("file_exists", help="File exists?")
    file_exists.add_argument("--filepath", '-f', required=True, help="Key or filepath")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(dest_key=args.dest_key, source_path=args.source_path)
    elif args.command == "download":
        download_file(src_file_name=args.src_file_name, dest_file_name=args.dest_file_name)
    elif args.command == "file_exists":
        file_exists(args.filepath)