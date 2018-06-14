import os


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:8420@localhost:5432/upload_txt_database"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    FLASKS3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    FLASKS3_DEBUG = True
    FLASKS3_ACTIVE = False
