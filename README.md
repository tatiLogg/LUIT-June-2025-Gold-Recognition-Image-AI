LUIT-June-2025-Gold-Recognition-Image-AI

An automated image recognition pipeline using Amazon Rekognition, DynamoDB, S3, and GitHub Actions.

> Automatically labels uploaded images and stores results in DynamoDB  
> Fully CI/CD automated via pull requests and merges to 'main'


Requirements

- Python 3.8+
- AWS account with Rekognition, S3, and DynamoDB enabled
- AWS IAM user with permissions for Rekognition, S3, and DynamoDB
- GitHub account + GitHub Actions enabled


AWS Setup Instructions

Create an S3 Bucket

Accessed the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/home) and created a bucket:

- Name: 'my-rekognition-pixel' 
- Region: 'us-east-1' recommended
- No public access required
- No versioning necessary

Created a folder inside the bucket: 'rekognition-input/'

Created DynamoDB Tables

Went to [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/home):

Created 2 tables:

Table Name         Partition Key  
'beta_results'     'filename (S)'
'prod_results'     'filename (S)'


Enabled Rekognition

Rekognition is enabled by default. Made sure my IAM user had these permissions:

```json
"rekognition:*",
"s3:*",
"dynamodb:*"

