# Load in our dependencies
import json
import time
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import threading
import unittest

import requests

from flask_json_multidict.test.utils.test_server import test_server


def request(**kwargs):
    """Helper to make our request with both Python 2 and 3"""
    # If we have data, coerce it to bytes
    pass


# DEV: This is extracted from `cassette`
#   https://github.com/uber/cassette/blob/0.3.6/cassette/tests/test_cassette.py#L95-L120
class TestFlaskJsonMultidict(unittest.TestCase):
    # Maintain a test server via a thread. This is shared across all test classes.
    test_server_thread = None

    @classmethod
    def setUpClass(cls):
        """Set up test server for all test cases"""
        # If we haven't started our test server yet, start it now
        if cls.test_server_thread is None:
            cls.test_server_thread = threading.Thread(
                target=test_server.run,
                kwargs={
                    'port': 9001
                }
            )
            # DEV: Daemonizing will kill the thread when python exits
            cls.test_server_thread.daemon = True
            cls.test_server_thread.start()

            # Wait for server to start
            tries = 0
            while True:
                # Attempt to contact our server
                tries += 1
                try:
                    requests.get('http://localhost:9001/', timeout=1)
                    break
                # If we fail to connect
                except:
                    # If this is a recent failure, try again in 100ms
                    if tries < 3:
                        time.sleep(0.1)
                        continue
                    # Otherwise, throw our error
                    raise

    def test_get(self):
        """
        A GET request to a server running `flask-json-multidict`
            is returned
        """
        # Make our request
        res = requests.get('http://localhost:9001/echo', timeout=2)
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'GET')

    def test_urlencoded(self):
        """
        A `application/x-www-form-urlencoded` request to a server running `flask-json-multidict`
            extracts the `form` data
        """
        # Make our request
        res = requests.post('http://localhost:9001/echo', headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        }, data='hello=world', timeout=2)
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertEqual(res_json['content-type'], 'application/x-www-form-urlencoded')
        self.assertEqual(res_json['body'], {'hello': 'world'})

    def test_multipart(self):
        """
        A `multipart/form-data` request to a server running `flask-json-multidict`
            extracts the `form` data
        """
        # Make our request
        # DEV: Force `multipart` via `files`
        res = requests.post('http://localhost:9001/echo', data={
            'hello': 'world',
        }, files={
            'textfile': (StringIO('hello'), 'hello.txt'),
        }, timeout=2)
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertRegexpMatches(res_json['content-type'], r'^multipart/form-data')
        self.assertEqual(res_json['body'], {'hello': 'world'})

    def test_json(self):
        """
        A `application/json` request to a server running `flask-json-multidict`
            extracts the `json` data
        """
        # Make our request
        res = requests.post('http://localhost:9001/echo', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'hello': 'world',
        }))
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertEqual(res_json['content-type'], 'application/json')
        self.assertEqual(res_json['body'], {'hello': 'world'})

    def test_list(self):
        """
        A `application/json` request to a server running `flask-json-multidict`
            with an array in its JSON
                extracts the array so it is accessible via `getlist`
        """
        # Make our request
        res = requests.post('http://localhost:9001/list', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'hello': ['world', 'moon'],
        }))
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertEqual(res_json['content-type'], 'application/json')
        self.assertEqual(res_json['body'], {'hello': ['world', 'moon']})

    def test_list_sublist_dict(self):
        """
        A `application/json` request to a server running `flask-json-multidict`
            with an array containing arrays and objects in its JSON
                silently ignores the nested structures
                allows other items through
        """
        # Make our request
        res = requests.post('http://localhost:9001/list', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'hello': ['world', ['nested'], {'foo': 'bar'}],
        }))
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertEqual(res_json['content-type'], 'application/json')
        self.assertEqual(res_json['body'], {'hello': ['world']})

    def test_dicts(self):
        """
        A `application/json` request to a server running `flask-json-multidict`
            with an object in its JSON
                silently ignores the dictionary
                allows other items through
        """
        # Make our request
        res = requests.post('http://localhost:9001/echo', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'hello': 'world',
            'nested': {'foo': 'bar'},
        }))
        self.assertEqual(res.status_code, 200)

        # Verify its attributes
        res_json = res.json()
        self.assertEqual(res_json['method'], 'POST')
        self.assertEqual(res_json['content-type'], 'application/json')
        self.assertEqual(res_json['body'], {'hello': 'world'})
