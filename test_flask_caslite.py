# -*- coding: utf-8 -*-
"""
    test_flask_caslite
    ~~~~~~~~~~~~~~~~
    :author: jooonwood@gmail.com
    :copyright: (c) 2019 by jooonwood.
    :license: MIT, see LICENSE for more details.
"""
import unittest
from flask import Flask, render_template_string, current_app, session
from flask_caslite import CasLite, login_required


class CasLiteTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)

        app.testing = True
        app.cas = CasLite(app)
        app.config.update(
            SECRET_KEY='hello',
            CAS_SERVER='https://sso.atbyd.com/cas'
        )
        @app.route('/')
        def index():
            return render_template_string('hello world!')

        @app.route('/private_page/', methods=['GET'])
        @login_required
        def private_page():
            cas_user = session.get('CAS_USERNAME', '')
            return 'Hello, ' + cas_user + session.get('hello', '')

        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'hello'
            password = 'password'

        return self.client.post('https://sso.atbyd.com/cas/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('https://sso.atbyd.com/cas/logout', follow_redirects=True)

    def tearDown(self):
        self.logout()
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

    def test_not_login(self):
        response = self.client.get('/private_page')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 308)
        self.assertIn('Redirecting...', data)
