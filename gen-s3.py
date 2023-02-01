#!/usr/bin/env python3
import boto3
import random
import string


s3 = boto3.client('s3', endpoint_url="http://localhost:4566")

# The name of the bucket
bucket_name = "s3-bucket-name"

# Create the bucket
s3.create_bucket(Bucket=bucket_name)

# The number of folders
num_folders = 50

# Loop over the number of folders
for i in range(num_folders):
    folder_name = "deployhash" + str(i) + "/"
    s3.put_object(Bucket=bucket_name, Key=folder_name + "index.html", Body=b"This is the index.html file.")
    s3.put_object(Bucket=bucket_name, Key=folder_name + "css/font.css", Body=b"This is the font.css file.")
    s3.put_object(Bucket=bucket_name, Key=folder_name + "image/hey.png", Body=b"This is the hey.png image.")
