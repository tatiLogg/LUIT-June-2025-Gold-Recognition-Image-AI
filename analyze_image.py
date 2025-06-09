import boto3
import os
import json
from decimal import Decimal
from datetime import datetime, timezone

# Load environment variables
TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION", "us-east-1")
BRANCH = os.getenv("GITHUB_HEAD_REF", "local-test")  # fallback to local-test

# Validate required env vars
if not TABLE_NAME or not BUCKET_NAME:
    raise EnvironmentError("Missing DYNAMO_TABLE_NAME or S3_BUCKET_NAME environment variable.")

# AWS clients
rekognition = boto3.client('rekognition', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.client('s3', region_name=REGION)

# Image details
image_filename = 'sample.jpg'  # You can make this dynamic if needed
local_path = f'images/{image_filename}'
s3_key = f"rekognition-input/{image_filename}"

# Upload to S3
print(f"Uploading {local_path} to S3 bucket {BUCKET_NAME}...")
s3.upload_file(local_path, BUCKET_NAME, s3_key)
print(f"✅ Uploaded to S3: s3://{BUCKET_NAME}/{s3_key}")

# Call Rekognition
print("Calling Amazon Rekognition...")
response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': s3_key}},
    MaxLabels=10,
    MinConfidence=80
)

# Prepare item for DynamoDB
print("Preparing item for DynamoDB...")
item = {
    "filename": s3_key,  # Must match the primary key of the DynamoDB table
    "labels": [
        {
            "Name": label["Name"],
            "Confidence": Decimal(str(label["Confidence"]))  # Convert float to Decimal
        }
        for label in response["Labels"]
    ],
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "branch": BRANCH
}

print("Item to write:", json.dumps(item, indent=2, default=str))

# Write to DynamoDB
print(f"Writing item to DynamoDB table: {TABLE_NAME}...")
table.put_item(Item=item)
print("✅ Successfully wrote label results to DynamoDB.")
