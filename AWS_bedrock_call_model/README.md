# model_demo
Call model in Amazon Bedrock

## 

Create consistent code documentation at scale with Amazon Bedrock Prompt Management. Watch how to automate your documentation workflow using foundation models while maintaining consistent standards across your team. See real implementation examples and learn how to get started with Amazon Bedrock Prompt Management.

# Amazon Bedrock Model Invocation Sample

## Description
This Python script demonstrates how to interact with Amazon Bedrock to invoke AI models using the AWS SDK (boto3). The sample shows how to set up a Bedrock client, make model invocations, and handle responses.

## Prerequisites
- Python 3.x
- AWS account with Bedrock access
- Configured AWS credentials
- Required Python packages:
  - boto3
  - os
  - dotenv
  - json

## Installation
1. Clone this repository
2. Install required packages:
   
```
pip install boto3
pip install dotenv
```

## Configuration

Before running the script, you need to:

- Copy and rename.env-example to .env
- Configure your AWS credentials within .env
- Update the credentials with your AWS profile
- Replace the modelId with your chosen Bedrock model ARN (optional)

## Features

- AWS Bedrock session initialization
- Model invocation 
- JSON request and response handling
- Support for code analysis use cases

## Security Notes

- Never commit AWS credentials in your code
- Use environment variables or AWS profiles for authentication
- Ensure proper IAM permissions are set up
