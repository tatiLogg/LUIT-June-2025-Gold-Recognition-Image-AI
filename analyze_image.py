import os
import boto3
from datetime import datetime

# ---------- Configuration ----------
AWS_REGION = os.getenv("AWS_REGION")
DYNAMO_TABLE = os.getenv("DYNAMO_TABLE")
S3_BUCKET = "my-rekognition-pixel"  #  Hardcoded correct bucket

if not AWS_REGION or not DYNAMO_TABLE:
    raise RuntimeError("Missing required AWS_REGION or DYNAMO_TABLE.")

# ---------- AWS Clients (using only .client) ----------
s3 = boto3.client("s3", region_name=AWS_REGION)
rekognition = boto3.client("rekognition", region_name=AWS_REGION)
dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

# ---------- Constants ----------
INPUT_PREFIX = "rekognition-input/"
IMAGES_FOLDER = "images"

# ---------- Main Logic ----------
def analyze_images():
    for filename in os.listdir(IMAGES_FOLDER):
        if not (filename.endswith(".jpg") or filename.endswith(".png")):
            continue

        local_path = os.path.join(IMAGES_FOLDER, filename)
        s3_key = INPUT_PREFIX + filename

        # Upload to S3
        s3.upload_file(local_path, S3_BUCKET, s3_key)
        print(f"Uploaded {filename} to s3://{S3_BUCKET}/{s3_key}")

        # Rekognition
        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": S3_BUCKET, "Name": s3_key}},
            MaxLabels=10,
            MinConfidence=80
        )

        labels = [{"Name": label["Name"], "Confidence": round(label["Confidence"], 2)}
                  for label in response["Labels"]]
        print(f"Detected Labels for {filename}:")
        for label in labels:
            print(f"- {label['Name']} ({label['Confidence']}%)")

        # Write to DynamoDB
        dynamodb.put_item(
            TableName=DYNAMO_TABLE,
            Item={
                "filename": {"S": s3_key},
                "labels": {"S": str(labels)},
                "timestamp": {"S": datetime.utcnow().isoformat() + "Z"},
                "branch": {"S": os.getenv("GITHUB_HEAD_REF", "main")}
            }
        )
        print(f"Saved results to DynamoDB table: {DYNAMO_TABLE}\n")

if __name__ == "__main__":
    analyze_images()