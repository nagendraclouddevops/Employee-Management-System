import pymssql
from config import DB_CONFIG


def get_connection():
    return pymssql.connect(
        server=DB_CONFIG["server"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )
