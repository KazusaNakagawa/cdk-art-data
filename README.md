
# Welcome to your CDK Python project!

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Verification method

```bash
# base64に変換
base64 -i <image>.png -o <image>.base64

# upload
$ curl -X POST <対象url> \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "art_data": "'"$(cat ./images/cat.base64)"'"
  }'

# output
{"message": "Image uploaded and metadata saved successfully", "item": {"UserId": "user123", "Timestamp": "2024-08-17T01:25:43", "S3Key": "user123/2024-08-17T01:25:43.png"}
```

### Check DynamoDB

```bash
# syntax
aws dynamodb scan \
    --table-name <YourTableName> \
    --region <your-region>

# ex
aws dynamodb scan \
    --table-name user-data-table \
    --region ap-northeast-1

# output
{
    "Items": [
        {
            "S3Key": {
                "S": "user123/2024-08-17T00:51:04.jpg"
            },
            "UserId": {
                "S": "user123"
            },
            "Timestamp": {
                "S": "2024-08-17T00:51:04"
            }
        }
    ],
    "Count": 1,
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```
