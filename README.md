# AWS Lambda Stock Alert using Docker Container

## Folder Structure:
```
lambda_stock_alert/
├── Dockerfile
├── lambda_function.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Steps to deploy:

### 1. Build and Run with Docker Compose:
```
docker-compose up --build
```

### 2. Test Lambda Locally:
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

### 3. Push Docker Image to AWS ECR:
```
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin xxxxxxx.dkr.ecr.us-east-2.amazonaws.com/trade
#aws ecr create-repository --repository-name stock-alert-image
docker tag stock-alert-lambda:latest xxxxx.dkr.ecr.us-east-2.amazonaws.com/trade/alert:v1
docker push xxxx.dkr.ecr.us-east-2.amazonaws.com/trade/alert:v1
```

### 4. Create AWS Lambda Function from Container Image:
- AWS Lambda Console → Create Function → Container Image (select image from ECR)

### 5. Set Environment Variables in Lambda:
```
STOCKS: AAPL,MSFT,GOOGL
TO_EMAIL: your_email@example.com
FROM_EMAIL: verified_email@example.com (SES verified)
```

### 6. Automate using EventBridge:
- Set a rule (e.g., every 15 minutes)

Your local and AWS environment is now set up for automated stock alerts!