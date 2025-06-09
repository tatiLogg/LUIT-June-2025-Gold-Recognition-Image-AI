import boto3
import os
from datetime import datetime

#CONFIGURATION
bucket_name = os.environ.get('S3_BUCKET_NAME', 'my-rekognition-pixel')  # Change if needed
region = os.environ.get('AWS_REGION', 'us-east-1')
input_folder = 'images/'

#Initialize AWS clients
s3 = boto3.client('s3', region_name=region)
rekognition = boto3.client('rekognition', region_name=region)

#Select the image to analyze
filename = 'sample.jpg'  # or replace with any of your PNG/JPG file names
local_path = os.path.join(input_folder, filename)
s3_key = f"rekognition-input/{filename}"

#Upload image to S3
s3.upload_file(local_path, bucket_name, s3_key)
print(f"✅ Uploaded {filename} to s3://{bucket_name}/{s3_key}")

#Call Rekognition to detect labels
response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
    MaxLabels=10,
    MinConfidence=70
)

#Display the detected labels
print("\n🔍 Detected Labels:")
for label in response['Labels']:
    print(f"- {label['Name']} ({label['Confidence']:.2f}%)")

#Timestamp for recordkeeping
timestamp = datetime.utcnow().isoformat()
print(f"\n🕒 Timestamp: {timestamp}")