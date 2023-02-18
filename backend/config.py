import os
from dotenv import load_dotenv


class Config:

    # load dotenv in the base root

    # refers to application_top
    APP_ROOT = os.path.join(os.path.dirname(__file__))
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    APP_NAME = os.getenv("APP_NAME")
    APP_URL = os.getenv("APP_URL")
    FLASK_ENV = os.getenv("FLASK_ENV")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    DB_CONNECTION_TYPE = os.getenv("DB_CONNECTION_TYPE")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = DB_CONNECTION_TYPE+"://"+DB_USERNAME + \
        ":"+DB_PASSWORD+"@"+DB_HOST+":"+DB_PORT+"/"+DB_DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = os.getenv("CORS_ORIGINS")

    DATA_PATH = os.path.join(APP_ROOT, os.getenv("DATA_PATH"))

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
