#!/usr/bin/env python3
import boto3
import datetime


def remove_old_folders(bucket_name, keep_x_folders, days, dry_run=False):
    """
    Deletes all S3 objects in folders older than `days_to_keep` in a specified S3 bucket.
    
    Parameters:
    bucket_name (str): The name of the S3 bucket.
    keep_x_folders (int): The number of newest folders to keep.
    days (int): The number of days folders to keep.
    dry_run (bool): If True, the script will only print the folders that would be deleted without deleting them.
    
    Returns:
    None
    """
    s3 = boto3.resource("s3", endpoint_url="http://host.docker.internal:4566")
    bucket = s3.Bucket(bucket_name)

    # Get a list of all folders
    result = bucket.meta.client.list_objects(Bucket=bucket_name, Delimiter='/')
    folders = [content["Prefix"] for content in result.get("CommonPrefixes", [])]

    if not folders:
        print(f"No folders found in the bucket '{bucket_name}'")
        return

    # Sort folders by the date in the folder name
    folders.sort(key=lambda folder: get_folder_date(bucket, folder), reverse=True)

    # Remove folders older than 30 days
    now = datetime.datetime.now(datetime.timezone.utc)
    folders_to_remove = [folder for folder in folders[keep_x_folders:]
                         if (now - get_folder_date(bucket, folder)).days >= days]

    if not folders_to_remove:
        print(f"No folders to remove.")
        return

    # Remove all other folders
    if dry_run:
        print(f'Would delete folders: {folders_to_remove}')
    else:
        for folder in folders_to_remove:
            objects_to_delete = [{'Key': obj.key} for obj in bucket.objects.filter(Prefix=folder)]
            bucket.delete_objects(Delete={'Objects': objects_to_delete})
            print(f'Deleted folder: {folder}')


def get_folder_date(bucket, folder):
    """
    Returns the date of the most recently modified object in a folder in a specified S3 bucket.
    
    Parameters:
    bucket (boto3.resources.factory.s3.Bucket): The boto3 S3 bucket object.
    folder (str): The name of the folder.
    
    Returns:
    datetime.datetime: The date of the most recently modified object in the folder.
    """
    objects = list(bucket.objects.filter(Prefix=folder).limit(1))
    obj = objects[0] if objects else None
    return obj.last_modified if obj else None


def lambda_handler(event, context):

    # Parse parameters from the `event` input
    s3_bucket_name = event['s3_bucket_name']
    x              = event['keep_x_folders']
    days_to_keep   = event['days_to_keep']
    dryrun         = event.get('dryrun', False)

    remove_old_folders(s3_bucket_name, x, days_to_keep, dryrun)
