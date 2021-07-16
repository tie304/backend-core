import uuid
from depends import get_s3_client
from botocore.exceptions import ClientError


from models.config import AWSConfig

aws_cfg = AWSConfig()


def upload_file(file: bytes) -> str:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = get_s3_client()
    try:
        obj_uid = str(uuid.uuid4())
        response = s3_client.upload_fileobj(file, aws_cfg.bucket_name, obj_uid)
        print(response)
    except ClientError as e:
        print(e)
        logging.error(e)
        raise HTTPException(status_code=500, detail="upload error")
    return obj_uid


def download_file(bucket_name, object_name, download_path):
    s3.download_file(bucket_name, object_name, download_path)
