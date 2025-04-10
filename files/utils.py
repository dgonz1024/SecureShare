import boto3
from django.conf import settings

def generate_presigned_url(file_key):
    """
    Generate a presigned URL for accessing a file in S3.
    :param file_key: The key (path) of the file in the S3 bucket.
    :return: A presigned URL for accessing the file.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_key,
        },
        ExpiresIn=3600  # URL expires in 1 hour
    )
    return url