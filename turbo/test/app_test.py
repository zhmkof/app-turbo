from __future__ import absolute_import, division, print_function, with_statement

import os
import signal
import sys
import unittest
import random
import time
import threading
import logging
import requests
import multiprocessing

from turbo.test.util import unittest

from turbo import app
from turbo.conf import app_config
from turbo import register

app_config.app_name = 'app_test'
app_config.web_application_setting = {}

#logger = logging.getLogger()


class HomeHandler(app.BaseBaseHandler):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class ApiHandler(app.BaseBaseHandler):

    _get_required_params = [
        ('skip', int, 0),
        ('limit', int, 20),
    ]

    _get_params = {
        'need': [
            ('action', None),
        ],
        'option': [
            ('who', basestring, 'python')
        ]
    }

    _post_required_params = [
        ('skip', int, 0),
        ('limit', int, 20),
    ]

    _post_params = {
        'need': [
            ('who', basestring),
        ],
    }

    def GET(self):
        self._params = self.parameter

        assert self._params['skip'] == 0
        assert self._params['limit'] == 20
        assert self._params['who'] == 'python'
        assert self._params['action'] is None

        self._data = {
            'value': self._params['who']
        }

    def POST(self):
        self._params = self.parameter
        print(self._params)

        assert self._params['skip'] == 0
        assert self._params['limit'] == 10

        self._data = {
            'value': self._params['who']
        }


    def PUT(self):
        self._data = {
            'api': {
                'put': 'value'
            }
        }


def run_server():
    register.register_url('/', HomeHandler)
    register.register_url('/api', ApiHandler)
    app.start()


class AppTest(unittest.TestCase):

    def setUp(self):
        server = multiprocessing.Process(target=run_server)
        server.start()
        self.home_url = 'http://localhost:8888'
        self.api_url = 'http://localhost:8888/api'
        self.pid = server.pid

    def tearDown(self):
        os.kill(self.pid, signal.SIGKILL)

    def test_get(self):
        resp = requests.get(self.home_url)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        resp = requests.post(self.home_url)
        self.assertEqual(resp.status_code, 200)


    def test_get_api(self):
        resp = requests.get(self.api_url)
        self.assertEqual(resp.status_code, 200)

        resp = requests.get(self.api_url)
        self.assertEqual(resp.status_code, 200)


    def test_post_api(self):
        resp = requests.post(self.api_url, data={'limit': 10, 'who': 'ruby'})
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.json()['res']['value'], 'ruby')



if __name__ == '__main__':
    unittest.main()