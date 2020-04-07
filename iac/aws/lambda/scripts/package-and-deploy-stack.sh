# PACKAGE LAMBDA FUNCTIONS AND UPLOAD TO S3
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket ga4gh-lambdas
# DEPLOY SERVERLESS STACK ON AWS
sam deploy --template-file packaged.yaml --stack-name refget-serverless --capabilities CAPABILITY_IAM --region us-east-2