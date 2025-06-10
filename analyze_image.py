import os
import boto3
from datetime import datetime

# ---------- Helper ----------
def get_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# ---------- Configuration ----------
AWS_REGION = get_env("AWS_REGION")
S3_BUCKET = get_env("S3_BUCKET_NAME")
DYNAMO_TABLE = get_env("DYNAMO_TABLE")

# ---------- AWS Clients ----------
s3 = boto3.client("s3", region_name=AWS_REGION)
rekognition = boto3.client("rekognition", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE)

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

        # Rekognition call
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
        item = {
            "filename": s3_key,
            "labels": labels,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "branch": os.getenv("GITHUB_HEAD_REF", "main")  # optional fallback
        }
        table.put_item(Item=item)
        print(f"Saved results to DynamoDB table: {DYNAMO_TABLE}\n")

if __name__ == "__main__":
    analyze_images()
