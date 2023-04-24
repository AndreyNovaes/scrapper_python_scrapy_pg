#!/bin/bash

SCRIPT_TO_RUN="script-to-setup-environment.sh"
REGION="us-west-1"
MAX_PRICE=0.01
KEY_PAIR_NAME="us-west-1"
SECURITY_GROUP_NAME="us-west-1"

function get_most_expensive_spot_instance_type_and_price() {
  local region="$1"
  local max_price="$2"
  aws ec2 describe-spot-price-history \
    --start-time "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --product-descriptions "Linux/UNIX" \
    --query "max_by(SpotPriceHistory[?SpotPrice!=null && to_number(SpotPrice)<=\`$max_price\` && !(starts_with(InstanceType, 't4g') || starts_with(InstanceType, 't4a') || starts_with(InstanceType, 'm6g') || starts_with(InstanceType, 'c6g')) && InstanceType!=null], &SpotPrice).{InstanceType: InstanceType, Price: SpotPrice}" \
    --output "text" \
    --region "$region"
}

function get_latest_amazon_linux_ami_id() {
  local region="$1"
  aws ec2 describe-images \
    --owners "amazon" \
    --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" "Name=state,Values=available" \
    --query "sort_by(Images[?CreationDate!=null],&CreationDate)[-1].ImageId" \
    --output "text" \
    --region "$region"
}

function get_security_group_id() {
  local region="$1"
  local SECURITY_GROUP_NAME="$2"
  aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" \
    --query "SecurityGroups[0].GroupId" \
    --output "text" \
    --region "$region"
}

INSTANCE_TYPE_AND_PRICE=$(get_most_expensive_spot_instance_type_and_price "$REGION" "$MAX_PRICE" )
INSTANCE_TYPE=$(echo "$INSTANCE_TYPE_AND_PRICE" | awk '{print $1}')
INSTANCE_PRICE=$(echo "$INSTANCE_TYPE_AND_PRICE" | awk '{print $2}')

BASE_AMI_ID=$(get_latest_amazon_linux_ami_id "$REGION")
SECURITY_GROUP_ID=$(get_security_group_id "us-west-1" "$SECURITY_GROUP_NAME")

echo "Region: $REGION"
echo "Instance type: $INSTANCE_TYPE"
echo "Price for the chosen instance: $INSTANCE_PRICE"

SPOT_INSTANCE_REQUEST_ID=$(aws ec2 request-spot-instances \
  --spot-price "$MAX_PRICE" \
  --instance-count 1 \
  --type "one-time" \
  --launch-specification "{
    \"ImageId\": \"$BASE_AMI_ID\",
    \"KeyName\": \"$KEY_PAIR_NAME\",
    \"InstanceType\": \"$INSTANCE_TYPE\",
    \"SecurityGroupIds\": [\"$SECURITY_GROUP_ID\"],
    \"UserData\": \"$(base64 --wrap=0 < script-to-setup-environment.sh)\"
  }" \
  --query 'SpotInstanceRequests[0].SpotInstanceRequestId' \
  --output text \
  --region "$REGION")

echo "Spot instance request ID: $SPOT_INSTANCE_REQUEST_ID"

echo "Waiting for spot instance request to be fulfilled..."
aws ec2 wait spot-instance-request-fulfilled \
  --spot-instance-request-ids "$SPOT_INSTANCE_REQUEST_ID" \
  --region "$REGION"

INSTANCE_ID=$(aws ec2 describe-spot-instance-requests \
  --spot-instance-request-ids "$SPOT_INSTANCE_REQUEST_ID" \
  --query 'SpotInstanceRequests[0].InstanceId' \
  --output text \
  --region "$REGION")

echo "Instance ID: $INSTANCE_ID"

echo "Waiting for instance to be running..."

echo "Waiting for SSH to be ready..."
sleep 5

while true; do
  INSTANCE_STATE=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --region "$REGION" --query 'Reservations[].Instances[].State.Name' --output text)
  
  if [ "$INSTANCE_STATE" = "running" ]; then
    echo "Instance is now running."
    break
  else
    echo "Instance not running yet, waiting for 5 seconds..."
    sleep 5
  fi
done

PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text \
  --region "$REGION")

echo "Public IP: $PUBLIC_IP"

echo "Copying script to run to the instance..."
scp -o StrictHostKeyChecking=no -i $KEY_PAIR_NAME.pem $SCRIPT_TO_RUN ec2-user@$PUBLIC_IP:~

echo "Waiting for instance to be ready..."
ssh -o StrictHostKeyChecking=no -i $KEY_PAIR_NAME.pem ec2-user@$PUBLIC_IP
