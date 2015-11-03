import boto3
import magic


def transfer(filepath, bucket, remote_path):
    client = boto3.client('s3')
    content_type = magic.from_file(filepath, True).decode(encoding='UTF-8')
    print(content_type)
    transfer = boto3.s3.transfer.S3Transfer(client)
    transfer.upload_file(filepath, bucket, remote_path, extra_args=
            {'ContentType': content_type})
