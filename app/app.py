#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api
from resources import UserRegistration, BucketListAll, BucketListId, BucketListItemAdd

app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegistration, '/auth/register')
api.add_resource(BucketListAll, '/bucketlists/')
api.add_resource(BucketListId, '/bucketlists/<list_id>/')
api.add_resource(BucketListItemAdd, '/bucketlists/<list_id>/items/')
# api.add_resource(BucketListResource,
#                  '/bucketlist/<list_id>',
#                  '/bucketlist/')
# api.add_resource( BucketListCreate, '/bucketlist')

if __name__ == '__main__':
    app.run(debug=True)
