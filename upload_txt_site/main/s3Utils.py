import boto3

'''
boto3 by default gets config from env variables
AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID
'''


def get_from_s3():
    s3client = boto3.client('s3')
    BUCKET_NAME = 'simple-site-rm-assets'
    KEY = 'static/GitHub-Mark-Light-120px-plus.png'

    f = s3client.get_object(Bucket=BUCKET_NAME, Key=KEY)["Body"].read()
    return f
