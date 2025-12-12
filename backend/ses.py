import os
import boto3
from dotenv import load_dotenv

load_dotenv()

ses = boto3.client(
    "ses",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "")
)
