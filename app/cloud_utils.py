import boto3
import os
from dotenv import load_dotenv
from flask_login import current_user
from flask import flash
import json

load_dotenv()


def create_s3_bucket():
    """
    Creates an S3 bucket in the specified region.

    Parameters:
    - bucket_name (str): The name of the bucket to be created.
    - region (str, optional): The AWS region in which to create the bucket. Default is 'us-east-1'.

    Returns:
    - A tuple of (bool, dict). The first element is a boolean indicating whether the bucket was created and the second element
        is the response from the S3 API if the bucket was created successfully, otherwise None.
    """
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    # Check if the bucket name is available
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True, "Bucket already exists."
    except Exception as exc:
        if exc.response["Error"]["Code"] == "404":
            # Create the bucket
            if region == "us-east-1":
                response = s3.create_bucket(Bucket=bucket_name)
            else:
                response = s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            return True, response
        return False, exc


def create_dynamodb_table():
    """Table that stores the file name and emails"""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    try:
        table = dynamodb.Table("files")
        return True, "Table already exists."
    except Exception as exc:
        if exc.response["Error"]["Code"] == "ResourceNotFoundException":
            table = dynamodb.create_table(
                TableName="files",
                KeySchema=[
                    {"AttributeName": "file_name", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "file_name", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            return True, "Table created successfully."
        return False, exc


def process_file(file, emails):
    """
    Uploads a file to an S3 bucket.

    Args:
        file (FileStorage): The file to be uploaded.
    """
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    emails = [email.strip() for email in emails.split(",")]
    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    s3.upload_fileobj(file, bucket_name, file.filename)
    # Save file name and emails in the Dynamo DB table
    presigned_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": file.filename},
        ExpiresIn=604800,
    )
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    table = dynamodb.Table("files")
    table.put_item(
        Item={
            "file_name": file.filename,
            "emails": emails,
            "uploadedby": current_user.email,
        }
    )
    lambda_client = boto3.client(
        "lambda",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    data = {
        "file_name": file.filename,
        "emails": emails,
        "uploadedby": current_user.email,
        "presigned_url": presigned_url,
        "Expiry": "604800",
    }
    payload = {"body": json.dumps(data)}
    resp = lambda_client.invoke(
        FunctionName="SendEmail",
        InvocationType="Event",
        Payload=json.dumps(payload),
    )
    if resp["StatusCode"] == 200 or resp["StatusCode"] == 202:
        flash("Emails sent successfully", "success")
    else:
        flash("Error sending emails", "warning")
    return True


if __name__ == "__main__":
    status, response = create_s3_bucket()
    if status:
        print(response)
    else:
        print(response)
        exit(1)
