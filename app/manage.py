#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api
from resources import UserRegistration, UserLogin, BucketListAll, BucketListId, BucketListItemAdd, BucketListItemEdit

app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegistration, '/auth/register/')
api.add_resource(UserLogin, '/auth/login/')
api.add_resource(BucketListAll, '/bucketlists/')
api.add_resource(BucketListId, '/bucketlists/<list_id>/')
api.add_resource(BucketListItemAdd, '/bucketlist/<list_id>/item/')
api.add_resource(BucketListItemEdit, '/bucketlist/<list_id>/item/<item_id>/')

if __name__ == '__main__':
    app.run(debug=True)
