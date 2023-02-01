# Answers

1. From my perspective we should run this script on an AWS Lambda function: You can create an AWS Lambda function in the same AWS region as the S3 bucket, upload the script as the function code, and trigger the function on a schedule. This option is useful if you want to automatically run the script at regular intervals, without the need to manage any infrastructure.
2. For testing purposes I create `dryrun` parameter which is `False` by default. If it is set to `True` the script will only print the folders that would be deleted without actually deleting them.
3. I implement `days_to_keep`  parameter which you can use if you want to keep folders not older than these number of days. You can put there `0` if you want to ignore this behaviour.

# Prerequisites

* Docker installed on your workstation

* Install localstack
```brew install localstack```

* Install awslocal cli
```pip install awscli-local```

# Local testing

Run localstack. Run it in separate terminal window to see the logs ouput.
```docker-compose up```

Create S3 bucket and generate some folders structure for testing
```python gen-s3.py```

Make archive of lambda_function.py
```zip lambda_function.zip lambda_function.py```

Create lambda
```
awslocal lambda create-function \
    --function-name rmOldFolders \
    --runtime python3.9 \
    --zip-file fileb://lambda_function.zip \
    --handler lambda_function.lambda_handler \
    --timeout 10 \
    --role localstack-role
```

Invoke lambda
```
awslocal lambda invoke \
    --function-name rmOldFolders \
    --cli-binary-format raw-in-base64-out \
    --payload file://events.json \
    ./output.json
```

# Production testing

For testing on real AWS account I'm using [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
```brew install aws-sam-cli```

Here is `template.yaml` in this repo used by SAM
```
---
AWSTemplateFormatVersion : '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  rmOldFolders:
    Type: AWS::Serverless::Function
    Properties:
      Handler: lambda_function.lambda_handler
      Runtime: python3.9
      Timeout: 10
```

Run this command to create lambda artifact
```sam build```

Run this command to invoke lambda function
```sam local invoke rmOldFolders -e events.json```

# Challenge description

As a member of the Infrastructure team, I want to cleanup old deployment folders in s3 to help manage AWS costs.
Write a script to remove all but the most recent X deployments. The script should take in X as a parameter.
If a deployment is older than X, we will delete the entire folder.
S3 folder bucket assets will look similar to below.

```
s3-bucket-name
  deployhash112/index.html
         /css/font.css
         /image/hey.png 
  dsfsfsl9074/index.html
         /css/font.css
         /image/hey.png 
  delkjlkploy3/index.html
         /css/font.css
         /image/hey.png 
  dsfff1234321/...
  klljkjkl123/...
```

## Questions

1. Where should we run this script?
2. How should we test the script before running it production?
3. If we want to add an additional requirement of deleting deploys older than 30 days while keeping X deployments. What additional changes would you need to make in the script?

## Notes

Consider using localstack to mimic s3.
List any assumptions made in a README.md
Please provide the github repo of the scripting project.

