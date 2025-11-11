import os
from dotenv import load_dotenv
import pymysql

# load environment variables from .env file
load_dotenv()

DB_CONNECT_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
    "port": int(os.environ["DB_PORT"]),
}

with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
    print("Connection Successful")
