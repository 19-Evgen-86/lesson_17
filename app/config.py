import os

DATABASE_PATH = os.path.join(os.getcwd(), "test.db")


class Config():
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    DEBUG = True
