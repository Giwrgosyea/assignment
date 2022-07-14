import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Lines" + "_secret_key")
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    ENVIRONMENT = "development"
    REQUEST_HOST = os.getenv("REQUEST_HOST") or "http://174.138.10.13:5000/api/"
    REDIS_SERVER = os.environ.get("REDIS_SERVER") or "localhost"
    REDIS_PORT = os.environ.get("REDIS_PORT") or "6379"
    # REDIS_URL = f"redis://{REDIS_SERVER}:{REDIS_PORT}"
    REDIS_URL = f"redis://{REDIS_SERVER}:{REDIS_PORT}"
    MONGO_DATABASE = "Lines"
    # MONGO_URI = "mongodb://" + MONGO_HOST + ":27017/" + MONGO_DATABASE
    MONGO_HOST = os.environ.get("MONGO_HOST") or "mongodb_container"

    MONGO_URI = (
        os.getenv("MONGO_URI") or "mongodb://" + MONGO_HOST + ":27017/" + MONGO_DATABASE
    )


key = Config.SECRET_KEY
config = Config()
