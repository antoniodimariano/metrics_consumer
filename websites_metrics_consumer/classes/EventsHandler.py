from psycopg2 import pool
import psycopg2.extras
import logging, os

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO
)
logger.setLevel(os.environ.get("logging_level", logging.INFO))


class ConnectionFromPool:
    """
    Class to manage the PostgreSQL Connection Pool and run queries

    """

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.connection = connection_pool.getconn()
        if self.connection:
            logger.debug(f"successfully received connection from connection pool {self.connection}")
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def write_query(self, query: str, params: tuple = None):
        """
        This method executes the given query and stores data into the DB
        :param query:
        :param params:
        :return:
        """
        try:
            self.cursor.execute(query, params)
            inserted_entry = self.cursor.fetchone()

        except Exception as error:
            logger.error('error executing query "{}", error: {}'.format(query, error))
            return None
        else:
            return inserted_entry

    def __del__(self):
        logger.debug(f"Put away a PostgreSQL connection {self.connection}")
        self.cursor.close()
        self.connection.commit()
        self.connection_pool.putconn(self.connection)


class EventHandler:
    def __init__(self, connection_params: str, min_thread: int = 1, max_thread: int = 200):
        self.connection_pool = pool.ThreadedConnectionPool(min_thread, max_thread, connection_params)
        if self.connection_pool:
            logger.info(f'Events DB Connection open {connection_params}')

    def store_event(self, event_payload: dict) -> bool:
        """
        This method exposes an high-level method that stores the given event_payload Dict
        into the DB.
        The client does nothing about how the DB is managed and what DB is being used.
        :param event_payload:
        :return:
        """
        try:
            import datetime
            from datetime import timezone

            url = event_payload.get('url')
            http_status = str(event_payload.get('http_status'))
            elapsed_time = str(event_payload.get('elapsed_time'))
            pattern_verified = str(event_payload.get('pattern_verified'))
            timestamp = datetime.datetime.now(timezone.utc).time().isoformat()
            query = "INSERT INTO metrics (url, http_status,elapsed_time, day, month, year, time,pattern_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING *"
            data_to_insert = (url, http_status, elapsed_time, datetime.date.today().day, datetime.date.today().month,
                              datetime.date.today().year, timestamp, pattern_verified)
            if ConnectionFromPool(self.connection_pool).write_query(query=query, params=data_to_insert):
                logger.info(f'Metric {data_to_insert} stored')
                return True
            else:
                logger.error(f'An error occurred storing {data_to_insert}')
                return True
        except Exception as error:
            logger.error(f"EXCEPTION {error} occurred storing the event {event_payload}")
            return False

    def __del__(self):
        logger.info("CLOSING ALL CONNECTIONS")
        self.connection_pool.closeall()
