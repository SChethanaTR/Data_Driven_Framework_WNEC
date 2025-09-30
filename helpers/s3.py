from pathlib import Path
import boto3
from helpers import ubuntu
import env

# AWS S3 basic configuration
REGION = env.region
BUCKET = env.bucket


def copy(origin, destination, fresh=False, ssh_host=None):
    """Copies a file from origin to destination
    If the file does not exist locally, it will be fetched from AWS S3 instance.
    Args:
        origin (string): S3 path
        destination (string): Destination path, can be just a directory
        fresh (bool, optional): Force a download even if a local copy exists. Defaults to False.
    """
    # Default directory can be optional, if omitted it will be added here
    if not origin.startswith("testdata/"):
        origin = f"testdata/{origin}"
    source_path = f"s3://{env.bucket}/{origin}"
    if fresh:
        ubuntu.delete_file_remote(f"/wneclient/QA/{origin}", ssh_host)
    if not ubuntu.is_file_exist_remote(f"/wneclient/QA/{origin}", ssh_host):
        ubuntu.is_execute_cmd_successful_remote(
            f"aws s3 cp {source_path} /wneclient/QA/{origin}", ssh_host
        )
    return ubuntu.is_execute_cmd_successful_remote(
        f"cp -r /wneclient/QA/{origin} {destination}", ssh_host
    )


def lists(bucket_folder_path):
    """Lists all files in the specified S3 bucket
    Args:
        bucket_folder_path (string): Path on S3 from which to retrieve children
    Returns:
        list: List of filenames
    """
    # Default directory can be optional, if omitted it will be added here
    if not bucket_folder_path.startswith("testdata/"):
        bucket_folder_path = f"testdata/{bucket_folder_path}"

    try:
        # Initiate session, this will raise an exception if the credentials are not set
        session = boto3.session.Session()

        # Initiate client, will raise an exception if the region is not valid
        s3 = session.client("s3", region_name=REGION)
        keylist = []
        paginator = s3.get_paginator("list_objects")

        for result in paginator.paginate(Bucket=BUCKET, Prefix=bucket_folder_path):
            for content in result.get("Contents", []):
                keylist.append(Path(content.get("Key")).name)
        return keylist
    except Exception as error:
        # Fails if any exception occurs
        print(f'[AWS] Failed to retrieve list of files from bucket: "{error}"')
        return False
