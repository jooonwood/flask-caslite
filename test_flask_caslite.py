# -*- coding: utf-8 -*-
"""
    test_flask_caslite
    ~~~~~~~~~~~~~~~~
    :author: jooonwood@gmail.com
    :copyright: (c) 2019 by jooonwood.
    :license: MIT, see LICENSE for more details.
"""
import unittest
from flask import Flask, render_template_string, current_app
from flask_caslite import CasLite


class CasLiteTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.testing = True
        self.cas = CasLite(app)

        @app.route('/')
        def index():
            return render_template_string('hello world!')

        self.context = app.app_context()
        self.context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_config(self):
        self.assertIn('CAS_SERVER', current_app.config)
        self.assertIn('CAS_VERSION', current_app.config)
        self.assertIn('CAS_TOKEN_SESSION_KEY', current_app.config)
        self.assertIn('CAS_USERNAME_SESSION_KEY', current_app.config)
        self.assertIn('CAS_ATTRIBUTES_SESSION_KEY', current_app.config)

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertEqual('hello world!', data)
