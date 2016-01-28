#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api
from resources import BucketListResource, UserRegistration

app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegistration, '/user/<id>', endpoint='user')
api.add_resource(
    BucketListResource, '/bucketlist/<id>', endpoint='bucketlist')

if __name__ == '__main__':
    app.run(debug=True)
