import os
from dotenv import load_dotenv

# Environment variables
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USE_S3 = False
    UPLOAD_FOLDER = "./data/images"

    SECRET_KEY = os.getenv("SESSION_SECRET")

class ProductionConfig:
    pass

class DevelopmentConfig(Config):
    DEBUG = True