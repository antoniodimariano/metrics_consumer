import unittest
from classes.EventsHandler import EventHandler
connections_params = 'postgresql://postgresql:test123@localhost/test?sslmode=disable'
class TestDB(unittest.TestCase):
    def setUp(self):
        self.handler = EventHandler(connection_params=connections_params)

    def test_a_test_valid_connection(self):
        event_payload = {"url": "http://cloudbased.me", "http_status": 200, "time": 0.2,
                         "content_verified": True}

        ret = self.handler.store_event(event_payload=event_payload)
        self.assertEqual(ret, True)

    def test_b_test_valid_connection(self):
        event_payload = {"cmcmcmcm": "http://cloudbased.me", "http_status": 200, "time": 0.2,
                         "content_verified": True}

        ret = self.handler.store_event(event_payload=event_payload)
        self.assertEqual(ret, True)

if __name__ == "__main__":
    unittest.main()
