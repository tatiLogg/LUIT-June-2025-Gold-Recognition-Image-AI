LUIT-June-2025-Gold-Recognition-Image-AI

Project Overview

Technologies Used

How It Works
1. Add an image to the 'images/' folder
2. Push or PR triggers GitHub Actions
3. Action:
   - Uploads image to 'rekognition-input/' in S3
   - Runs Rekognition on the image
   - Saves labels to:
     - 'beta_results' table on **PR**
     - 'prod_results' table on **merge**

CI/CD Workflows

Pull Request: 'on_pull_request.yml'
- Triggers when a PR targets 'main'
- Writes results to 'beta_results' table

Merge to Main: 'on_merge.yml'
- Triggers on push to 'main'
- Writes results to 'prod_results' table

DynamoDB Schema

Table Names:
- 'beta_results'
- 'prod_results'

Partition Key:
- 'filename' (string)

GitHub Secrets (Required)


Secret Name                   Description                      
'AWS_ACCESS_KEY_ID'           AWS IAM access key               
'AWS_SECRET_ACCESS_KEY'       AWS IAM secret                   
'AWS_REGION'                  e.g. 'us-east-1' 


Sample Output (JSON)
```json
{
  "filename": "rekognition-input/sample.jpg",
  "labels": [
    {"Name": "Cat", "Confidence": 95.23},
    {"Name": "Animal", "Confidence": 93.76}
  ],
  "timestamp": "2025-06-01T14:55:32Z",
  "branch": "main"
}
