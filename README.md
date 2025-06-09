LUIT-June-2025-Gold-Recognition-Image-AI

An automated image recognition pipeline using Amazon Rekognition, DynamoDB, S3, and GitHub Actions.
> Automatically labels uploaded images and stores results in DynamoDB  
> Fully CI/CD automated via pull requests and merges to "main"


Requirements
- Python 3.8+
- AWS account with Rekognition, S3, and DynamoDB enabled
- AWS IAM user with permissions for Rekognition, S3, and DynamoDB
- GitHub account + GitHub Actions enabled


AWS Setup Instructions
Create an S3 Bucket:

Go to the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/home) and create a bucket:

- Name: 'my-rekognition-pixel' (or your own)
- Region: 'us-east-1' recommended
- No public access required
- No versioning necessary

Create a folder inside the bucket: 'rekognition-input/'


Create DynamoDB Tables

Go to the [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/home):

Create 2 tables:

| Table Name     | Partition Key   |
|----------------|-----------------|
| 'beta_results' | 'filename (S)'  |
| 'prod_results' | 'filename (S)'  |

Make sure the key name is exactly 'filename' and of type 'String'.


Enable Rekognition

Rekognition is enabled by default. Make sure your IAM user has these permissions:

```json
"rekognition:*",
"s3:*",
"dynamodb:*"
````


You can use the managed policy: 'AmazonRekognitionFullAccess'.


Configure GitHub Secrets

Navigate to your repo:
Settings → Secrets and variables → Actions → New repository secret

Create the following:

 Name                     Example Value              
 'AWS_ACCESS_KEY_ID'      'AKIAIOSFODNN7EXAMPLE'     
 'AWS_SECRET_ACCESS_KEY'  'wJalrXUtnFEMI/K7MDENG...' 
 'AWS_REGION'             'us-east-1'                
 'S3_BUCKET_NAME'         'my-rekognition-pixel'     
 'DYNAMODB_TABLE_BETA'    'beta_results'             
 'DYNAMODB_TABLE_PROD'    'prod_results'             



How to Add and Analyze Images

1. Add any '.jpg' or '.png' to the 'images/' folder in your repo
2. Commit and push to a new branch
3. Open a pull request to 'main'

GitHub Actions will:
Upload the image to S3
Run Amazon Rekognition
Save detected labels to DynamoDB

Example:

```bash
# Add image
cp cat.png images/

# Commit and push
git checkout -b analyze-cat
git add .
git commit -m "Add cat image"
git push origin analyze-cat
```

Open a PR in GitHub → Done


How to Verify Data in DynamoDB

1. Open the AWS Console → DynamoDB → Tables
2. Choose either 'beta_results' or 'prod_results'
3. Click Explore table items
4. You should see an entry like:

```json
{
  "filename": "rekognition-input/cat.png",
  "labels": [
    {"Name": "Cat", "Confidence": 97.5},
    {"Name": "Animal", "Confidence": 93.3}
  ],
  "timestamp": "2025-06-08T18:35:00Z",
  "branch": "main"
}
```

Trigger Type  Table Used    
Pull Request   'beta_results' 
Merge to Main  'prod_results' 



Folder Structure

```
 .github/workflows
│   ├── on_pull_request.yml  # CI for PRs
│   └── on_merge.yml         # CI for merges
 images/
│   └── sample.jpg           # Your test images
 analyze_image.py          # Python script
 README.md
```


Sample Output

```bash
✅ Uploaded sample.jpg to s3://my-rekognition-pixel/rekognition-input/sample.jpg

🔍 Detected Labels:
- Cat (97.5%)
- Animal (93.3%)

Timestamp: 2025-06-08T18:35:00Z
```


References:-

[Amazon Rekognition](https://docs.aws.amazon.com/rekognition/)
[DynamoDB](https://docs.aws.amazon.com/dynamodb/)
[GitHub Actions](https://docs.github.com/en/actions)





Repo Link:
Medium: https://medium.com/p/5ffafdc6834b/edit


