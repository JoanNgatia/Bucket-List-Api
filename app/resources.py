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
# parser.add_argument('user', type=str)
# parser.add_argument('bucketlist', type=str)
# parser.add_argument('bucketlistitem', type=str)


class UserRegistration(Resource):
    def post(self):
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        username = args['username']
        password = args['password']

        exists = session.query(User).filter_by(username).first()
        if exists:
            return {'message': 'User already exists!'}
        else:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()
            return {'message': 'User has been successfully registered'}


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
        parser.add_argument('list_name')
        args = parser.parse_args()
        list_name = args['list_name']

        bucketlistexist = session.query(BucketList).filter_by(
            BucketList.list_name == list_name).first()
        if bucketlistexist:
            return {'message': 'Bucketlist  already exists'}
        else:
            bucketlist = BucketList(list_name=list_name)
            session.add(bucketlist)
            session.commit()
            return bucketlist, 201
