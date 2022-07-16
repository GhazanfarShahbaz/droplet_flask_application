import boto3
import os

from typing import Dict

function_mapper = {
    "client": boto3.client,
    "resource": boto3.resource
}


def get_aws_credentials() -> Dict[str, str]:
    return {
        "AWS_FILE_SERVICE":  os.getenv("AWS_FILE_SERVICE"),
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
        "AWS_PASSWORD": os.getenv("AWS_PASSWORD"),
        "AWS_REGION_NAME": os.getenv("AWS_REGION_NAME"),
    }


def get_aws_client_or_resource(type: str):
    credentials: Dict[str, str] = get_aws_credentials()

    client_or_resource = function_mapper[type](
        credentials["AWS_FILE_SERVICE"],
        aws_access_key_id=credentials["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=credentials["AWS_ACCESS_KEY"],
        region_name=credentials["AWS_REGION_NAME"],
    )
    
    return client_or_resource


def upload_file(file, content_type) -> str:
    client = get_aws_client_or_resource("client")
    bucket_name: str = os.getenv("AWS_BUCKET_NAME")

    try:
        client.put_object(
            Body=file,
            Bucket=bucket_name,
            Key=f"server_files/{file.filename}",
            # Key= f"server_files/{file.filename}",
            ContentType=content_type
        )
    except:
        return "failed to upload file"

    return "success"


def delete_file(bucket_name: str, file_path: str) -> str:
    client = get_aws_client_or_resource("client")

    client.delete_object(
        Bucket=bucket_name,
        Key=file_path
    )

    return "Success"