import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost:5432/MemoryVaultLocal'
    SQLALCHEMY_TRACK_MODIFICATIONS = False