import pymysql

from ..dependencies import DB_CONNECT_CONFIG


def setup_db():
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "api/sql/crud_ops/delete/drop_all.sql", "r"
    ) as sql_drop_all, open(
        "api/sql/schema/create_tables.sql", "r"
    ) as sql_create_tables, open(
        "api/sql/triggers/create_holdings_trigger.sql", "r"
    ) as sql_create_holdings_trigger:
        cursor = conn.cursor()

        try:
            cursor.execute(sql_drop_all.read())
            cursor.execute(sql_create_tables.read())
            cursor.execute(sql_create_holdings_trigger.read())
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Database setup failed: {e}")

        finally:
            cursor.close()


def db_fill_starter_data():
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "api/sql/insert_sample_data.generated.sql", "r"
    ) as sql_insert_sample_data:
        cursor = conn.cursor()

        try:
            cursor.execute(sql_insert_sample_data.read())
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Database insert failed: {e}")

        finally:
            cursor.close()
