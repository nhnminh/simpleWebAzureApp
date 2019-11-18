import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_file(file_name, blob_service_client, container_name):
    """
    Function to upload a file to an S3 bucket / Azure Storage Model
    """
    # object_name = file_name
    # s3_client = boto3.client('s3')
    # response = s3_client.upload_file(file_name, bucket, object_name)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    # Upload the created file
    with open(file_name, "rb") as data:
        blob_client.upload_blob(data)

    return blob_client

