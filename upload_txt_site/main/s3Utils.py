import boto3
from botocore.client import Config
import secrets
import os
'''
boto3 by default gets config from env variables
AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID
'''


def get_from_s3(BUCKET_NAME, KEY):
    s3 = boto3.client('s3')
    fBytes = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)["Body"].read()
    with open("testSave.png", "wb") as testSaveFile:
        testSaveFile.write(fBytes)

    return None


def save_to_s3(BUCKET_NAME, folder, form_file):
    random_hex = secrets.token_hex(8)
    s3 = boto3.client('s3')
    f_n, f_ext = os.path.splitext(form_file.filename)
    KEY = folder + "/" + f_n + random_hex + f_ext
    s3.put_object(Bucket=BUCKET_NAME, Body=form_file, Key=KEY)
    return KEY


def s3_url_for(BUCKET_NAME, KEY):
    s3 = boto3.client('s3', "us-east-2",
                      config=Config(signature_version='s3v4'))
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': KEY})
    return url


if __name__ == "__main__":
    BUCKET_NAME = 'simple-site-rm-assets'
    KEY = 'static/main.css'
    url = s3_url_for(BUCKET_NAME, KEY)
    print(url)
