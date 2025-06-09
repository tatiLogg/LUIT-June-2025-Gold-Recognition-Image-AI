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

Configure GitHub Secrets
Navigate to your repo:
Settings → Secrets and variables → Actions → New repository secret

Create the following:
Name	                    Example Value
AWS_ACCESS_KEY_ID	        AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY	    wJalrXUtnFEMI/K7MDENG...
AWS_REGION	              us-east-1
S3_BUCKET_NAME	          my-rekognition-pixel
DYNAMODB_TABLE_BETA	      beta_results
DYNAMODB_TABLE_PROD	      prod_results

How to Add and Analyze Images
Add any .jpg or .png to the images/ folder in your repo
Commit and push to a new branch
Open a pull request to main

GitHub Actions will:
Upload the image to S3
Run Amazon Rekognition
Save detected labels to DynamoDB

# Add image
cp cat.png images/

# Commit and push
git checkout -b analyze-cat
git add .
git commit -m "Add cat image"
git push origin analyze-cat

Open a PR in GitHub → Done!

How to Verify Data in DynamoDB
Open the AWS Console → DynamoDB → Tables
Choose either beta_results or prod_results
Click Explore table items
You should see an entry like:

{
  "filename": "rekognition-input/cat.png",
  "labels": [
    {"Name": "Cat", "Confidence": 97.5},
    {"Name": "Animal", "Confidence": 93.3}
  ],
  "timestamp": "2025-06-08T18:35:00Z",
  "branch": "main"
}

Trigger Type	Table Used
Pull Request	beta_results
Merge to Main	prod_results


Folder Structure

  .github/workflows
│   ├── on_pull_request.yml  # CI for PRs
│   └── on_merge.yml         # CI for merges
 images/
│   └── sample.jpg           # Your test images
  analyze_image.py          # Python script
 README.md

Sample Output
Uploaded sample.jpg to s3://my-rekognition-pixel/rekognition-input/sample.jpg

Detected Labels:
- Cat (97.5%)
- Animal (93.3%)

Timestamp: 2025-06-08T18:35:00Z

References
Amazon Rekognition
DynamoDB
GitHub Actions

Contributing
Feel free to fork and expand the labeling logic, DynamoDB structure, or UI output. PRs welcome!

Repo Link
GitHub: tatiLogg/LUIT-June-2025-Gold-Recognition-Image-AI

