from psycopg2 import pool
import psycopg2
import psycopg2.extras
import unittest


class TestDB(unittest.TestCase):
    def setUp(self):
        self.connection_pool = pool.ThreadedConnectionPool(1, 2, database='test', user='postgresql', password='test123',
                                                           host='localhost')

    def tearDown(self):
        self.connection_pool.closeall()

    def test_a_ThreadedPool_Connection(self):
        self.assertEqual(self.connection_pool.closed, False)
        self.assertEqual(self.connection_pool.maxconn, 2)
        self.assertEqual(self.connection_pool.minconn, 1)

    def test_b_test_Write(self):
        connection_1 = self.connection_pool.getconn()
        query = "INSERT INTO metrics (url, http_status,elapsed_time, day, month, year, pattern_verified) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING *"
        params = ("http://test.com", '200', '0.2', '02', '10', '2021', 'True')
        cursor_1 = connection_1.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_1.execute(query, params)
        connection_1.commit()
        inserted_entry = cursor_1.fetchone()
        self.assertIsNotNone(inserted_entry)
        cursor_1.close()
        self.assertEqual(cursor_1.closed, True)

    def test_c_test_Read(self):
        connection_2 = self.connection_pool.getconn()
        cursor_2 = connection_2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_2.execute("select * from metrics")
        records = cursor_2.fetchmany(1)
        cursor_2.close()
        self.assertIsNotNone(records)
        self.assertEqual(cursor_2.closed, True)


if __name__ == "__main__":
    unittest.main()
