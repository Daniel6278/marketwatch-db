import pymysql, logging

from ..dependencies import DB_CONNECT_CONFIG, DatabaseError


def setup_db(logger: logging.Logger):
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
            logger.info("Database tables (re)created.")

        except Exception as e:
            conn.rollback()
            logger.error(f"Database setup failed: {e}")
            raise DatabaseError(
                ("drop_all.sql", "create_tables.sql", "create_holdings_trigger.sql")
            )

        finally:
            cursor.close()


def db_fill_starter_data(logger: logging.Logger):
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "api/sql/insert_sample_data.generated.sql", "r"
    ) as sql_insert_sample_data:
        cursor = conn.cursor()

        try:
            cursor.execute(sql_insert_sample_data.read())
            conn.commit()
            logger.info("Database filled with starter data.")

        except Exception as e:
            conn.rollback()
            logger.error(f"Database insert failed: {e}")
            raise DatabaseError(("insert_sample_data.generated.sql"))

        finally:
            cursor.close()
