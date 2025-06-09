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
Create an S3 Bucket:
Accessed the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/home) and created a bucket:

- Name of my bucket: 'my-rekognition-pixel' 
- Region: 'us-east-1' recommended
- No public access required
- No versioning necessary

Created a folder inside the bucket: 'rekognition-input/'

Created DynamoDB Tables:
Went to [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/home):

Created 2 tables:
Table Name         Partition Key  
1. 'beta_results'     'filename (S)'
2. 'prod_results'     'filename (S)'


Configured GitHub Secrets
Navigated to my repo:
Settings → Secrets and variables → Actions → New repository secret

Created the following:
Name	                    Example Value
AWS_ACCESS_KEY_ID	        AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY	    wJalrXUtnFEMI/K7MDENG...
AWS_REGION	              us-east-1
S3_BUCKET_NAME	          my-rekognition-pixel
DYNAMODB_TABLE_BETA	      beta_results
DYNAMODB_TABLE_PROD	      prod_results

How to Add and Analyze Images
Add any .jpg or .png to the images/ folder in your repo (I dragged my images to a folder I labelled for the images)
Committed and pushed to a new branch
Opened a pull request to main

GitHub Actions will:
Upload the image to S3
Run Amazon Rekognition
Save detected labels to DynamoDB

Added an image
cp cat.png images/

Committed and pushed
git checkout -b analyze-cat
git add .
git commit -m "Add cat image"
git push origin analyze-cat

Opened a PR in GitHub → Completed task

How to Verify Data in DynamoDB
Opened the AWS Console → DynamoDB → Tables
Chose either beta_results or prod_results
Clicked Explore table items
Example of what entry I expected to view:

{
  "filename": "rekognition-input/cat.png",
  "labels": [
    {"Name": "Cat", "Confidence": 97.5},
    {"Name": "Animal", "Confidence": 93.3}
  ],
  "timestamp": "2025-06-08T18:35:00Z",
  "branch": "main"
}

Trigger Type	Table Used:
- Pull Request	beta_results
- Merge to Main	prod_results


Folder Structure:

  .github/workflows
│   ├── on_pull_request.yml  # CI for PRs
│   └── on_merge.yml         # CI for merges
 images/
│   └── sample.jpg           # Your test images
  analyze_image.py          # Python script
 README.md

Sample Output:
Uploaded sample.jpg to s3://my-rekognition-pixel/rekognition-input/sample.jpg

Detected Labels:
- Cat (97.5%)
- Animal (93.3%)

Timestamp: 2025-06-08T18:35:00Z

References
Amazon Rekognition
DynamoDB
GitHub Actions


Medium Link: 
GitHub: tatiLogg/LUIT-June-2025-Gold-Recognition-Image-AI

Configured GitHub Secrets
Navigated to my repo:
Settings → Secrets and variables → Actions → New repository secret

Created the following:
Name	                    Example Value
AWS_ACCESS_KEY_ID	        AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY	    wJalrXUtnFEMI/K7MDENG...
AWS_REGION	              us-east-1
S3_BUCKET_NAME	          my-rekognition-pixel
DYNAMODB_TABLE_BETA	      beta_results
DYNAMODB_TABLE_PROD	      prod_results


Enabled Rekognition

Rekognition is enabled by default. Made sure my IAM user had the following permissions:

```json
"rekognition:*",
"s3:*",
"dynamodb:*"



GitHub: tatiLogg/LUIT-June-2025-Gold-Recognition-Image-AI

