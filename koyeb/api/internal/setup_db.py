import pymysql

from ..dependencies import DB_CONNECT_CONFIG


def setup_db():
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "sql/ops/authenticate_user.sql", "r"
    ) as query:
        cursor = conn.cursor()
