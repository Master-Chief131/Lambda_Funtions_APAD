#!/bin/bash

# Load jq if not already installed
command -v jq >/dev/null 2>&1 || { echo >&2 "jq is required but it's not installed. Aborting."; exit 1; }

# Read the configuration file
CONFIG_FILE="lambda_config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Configuration file not found!"
  exit 1
fi

# Iterate over each function in the configuration file
for FUNCTION in $(jq -c '.functions[]' "$CONFIG_FILE"); do
  NAME=$(echo "$FUNCTION" | jq -r '.name')
  PATH=$(echo "$FUNCTION" | jq -r '.path')
  MAIN_FILE=$(echo "$FUNCTION" | jq -r '.main_file')
  ENV_PATH=$(echo "$FUNCTION" | jq -r '.env_path')

  echo "Updating Lambda function: $NAME"

  # Fetch parameters from SSM Parameter Store and write to .env file
  aws ssm get-parameters-by-path --path "$ENV_PATH" --region us-west-2 | jq -r '.Parameters | map(.Name+"="+.Value)| join("\n") | sub("/Test-LAMBDA/"; ""; "g")' > .env

  # Create a temporary directory for packaging the Lambda function
  mkdir -p /tmp/lambda/"$NAME"

  # Copy files to the temporary directory
  echo "Copying Files from Project to Temp Folder"
  rsync -a "$PATH"/ /tmp/lambda/"$NAME"/

  # Rename the main file to lambda_function.py
  mv /tmp/lambda/"$NAME"/"$MAIN_FILE" /tmp/lambda/"$NAME"/lambda_function.py

  # Copy .env file to the temporary directory
  cp .env /tmp/lambda/"$NAME"/.env

  # Navigate to the temporary directory and zip the contents
  cd /tmp/lambda/"$NAME"/ && zip -rq ../"$NAME".zip .

  # Upload the zip file to S3
  aws s3 cp /tmp/lambda/"$NAME".zip s3://your-bucket/lambda_functions/"$NAME"/"$NAME".zip

  # Update the Lambda function code
  aws lambda update-function-code --function-name "$NAME" --s3-bucket your-bucket --s3-key lambda_functions/"$NAME"/"$NAME".zip

  # Clean up temporary files (optional but recommended)
  rm -rf /tmp/lambda/"$NAME"
  rm .env

  echo "Lambda function $NAME updated successfully"
done
