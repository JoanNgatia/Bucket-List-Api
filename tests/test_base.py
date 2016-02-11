from flask import Flask
from flask.ext.testing import TestCase

from app.manage import api

class TestBase(TestCase):

    def create_app(self):

        api.config['TESTING'] = True
        return api
