import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_database_connection():
    db_config = {
        "host": os.environ.get("HOST"),
        "user": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD"),
        "database": os.environ.get("DATABASE"),
    }
    connection = mysql.connector.connect(**db_config)
    return connection
