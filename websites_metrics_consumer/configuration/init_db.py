import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def init_db(db_user, db_password, db_host, db_port, db_name, db_table):
    connection = psycopg2.connect(dbname=db_name, host=db_host, port=db_port, user=db_user, password=db_password)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    r = cursor.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name))
    )

    create_table = (
            "CREATE TABLE " + db_table + " (id serial NOT NULL PRIMARY KEY, url TEXT, http_status TEXT, day TEXT, month TEXT, year TEXT, time TEXT, elapsed_time TEXT, pattern_verified TEXT)")

    cursor.execute(sql.SQL(create_table)
                   )

    return True


if __name__ == "__main__":
    init_db(db_user='postgresql', db_password='test123', db_host='192.168.1.103', db_port=5432, db_name='metrics',
            db_table='metrics')
