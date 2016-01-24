from models import User, BucketList, BucketListItems
from db import session

from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with

users = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String
}

bucketlists = {
    'list_id': fields.Integer,
    'list_name': fields.String,
    'items': fields.String,
    'creator': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

bucketlistitems = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'creator': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('bucketlist', type=str)
parser.add_argument('bucketlistitem', type=str)


class BucketListResource(Resource):
    @marshal_with(bucketlists)
    def get(self, id):
        bucketlist = session.query(BucketList).filter(
            BucketList.list_id == id).first()
        if not bucketlist:
            abort(404, message="Bucketlist {} does not exist".format(id))
        return bucketlist

    @marshal_with(bucketlists)
    def put(self, id):
        parsed_args = parser.parse_args()
        bucketlist = session.query(BucketList).filter(
            BucketList.list_id == id).first()
        bucketlist.items = parsed_args['items']
        session.add(bucketlist)
        session.commit()
        return bucketlist, 201
