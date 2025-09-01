import json
import boto3
import os

sns = boto3.client("sns")

# Set this as a Lambda environment variable
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        # Parse body from API Gateway
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No request body"})
            }

        body = json.loads(event["body"])

        name = body.get("name", "N/A")
        email = body.get("email", "N/A")
        subject = body.get("subject", "No subject")
        message = body.get("message", "")

        # Build email content
        msg = (
            f"New Contact Form Submission\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}"
        )

        # Publish to SNS topic
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Contact Form: {subject}",
            Message=msg
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "success", "message": "Sent!"})
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": str(e)})
        }
