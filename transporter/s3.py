import boto3


def transfer(filepath, bucket, remote_path):
    client = boto3.client('s3')
    transfer = boto3.s3.transfer.S3Transfer(client)
    transfer.upload_file(filepath, bucket, remote_path)
