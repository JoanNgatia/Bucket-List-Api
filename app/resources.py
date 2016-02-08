from sqlalchemy import DateTime
from models import User, BucketList, BucketListItems
from db import session

from flask import g, request
# from flask_httpauth import HTTPBasicAuth
from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with, marshal
from flask.ext.login import LoginManager, login_required, current_user
# from manage import login_manager
# from sqlalchemy_paginator import Paginator

# auth = HTTPBasicAuth()

users = {
    'user_id': fields.Integer,
    'username': fields.String,
    'password_hash': fields.String
}

bucketlistitems = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'creator': fields.String,
    # 'bucket_id': fields.Integer,
    'done': fields.Boolean
    # 'date_created': fields.DateTime,
    # 'date_modified': fields.DateTime
}

bucketlists = {
    'id': fields.Integer(attribute='list_id'),
    'list_name': fields.String,
    'items': fields.Nested(bucketlistitems),
    # 'creator': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}


parser = reqparse.RequestParser()




class UserRegistration(Resource):
    """Resource to handle '/auth/register/' endpoint."""

    def post(self):
        """Allow a user to register."""
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        exists = session.query(User).filter_by(username=username).first()
        if exists:
            return {'message': 'User already exists!'}
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        return {'message': 'User {} has been successfully registered'
                           .format(username)}


class UserLogin(Resource):
    """Resource to handle '/auth/login/' endpoint."""

    def post(self):
        """Log in a user."""
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password_hash = args['password']

        userlogged = session.query(User).filter_by(username=username).first()
        if userlogged:
            if userlogged.verify_password(password_hash):
                token = userlogged.generate_confirmation_token()
                userlogged.confirmed = True
                session.add(userlogged)
                session.commit()
                return {'token': token}
            # if password not verified
            return {'message': 'Password not verified'}
        # if user doesn't exist
        return {'message': "User doesn't exist"}


class BucketListAll(Resource):

    """
    Resource to handle '/bucketlists/' and
    '/bucketlists/<int:page>' endpoint.
    """

    @login_required
    def get(self):
        """Retrieve all bucketlists belonging to the logged in user."""
        # parser.add_argument('page')
        # args = parser.parse_args()
        # pageshow = args[page]
        # limit = 20
        created_by = current_user.user_id
        bucketlist = session.query(BucketList).filter_by(creator=created_by).all()
        return marshal(bucketlist, bucketlists)

    @login_required
    def post(self):
        """Create a new bucketlist."""
        parser.add_argument('list_name')
        args = parser.parse_args()
        list_name = args['list_name']
        bucketlistexist = session.query(BucketList).filter_by(
            list_name=list_name).first()
        created_by = current_user.user_id
        if bucketlistexist:
            return {'message': 'Bucketlist  already exists'}
        else:
            bucketlist = BucketList(list_name=list_name, creator=created_by)
            session.add(bucketlist)
            session.commit()
            return marshal(bucketlist, bucketlists), 201


class BucketListId(Resource):
    """Resource to handle '/bucketlist/<list_id>' endpoint."""

    @login_required
    def get(self, list_id):
        """Retrieve a particular bucketlist belonging to logged in user."""
        bucketlist = session.query(BucketList).filter_by(
            list_id=list_id).first()
        if bucketlist:
            return marshal(bucketlist, bucketlists)

        return {'message': 'Bucketlist {} does not exist'.format(list_id)}

    @login_required
    def put(self, list_id):
        """Modify existing bucketlist."""
        bucketlistedit = session.query(
            BucketList).filter_by(list_id=list_id).first()
        if bucketlistedit:
            parser.add_argument('list_name')
            args = parser.parse_args()
            bucketlistedit.list_name = args['list_name']
            session.add(bucketlistedit)
            session.commit()
            return {'message': 'Bucketlist {} has been modified'
                               .format(list_id)}
        return {'message': 'Bucketlist {} has not been found'
                .format(list_id)}

    @login_required
    def delete(self, list_id):
        """Delete an existing bucketlist."""
        bucketlistdelete = session.query(
            BucketList).filter_by(list_id=list_id).first()
        session.delete(bucketlistdelete)
        session.commit()
        return {'message': 'Bucketlist {} has been deleted'.format(list_id)}


class BucketListItemAdd(Resource):
    """Resource to handle '/bucketlist/<list_id>/item'."""

    @login_required
    def post(self, list_id):
        """Add a new item to a bucketlist."""
        bucketlistfind = session.query(
            BucketList).filter_by(list_id=list_id).first()
        if bucketlistfind:
            parser.add_argument('item_name')
            args = parser.parse_args()
            item = args['item_name']
            bucketlistitem = BucketListItems(
                item_name=item, bucketlist=bucketlistfind)
            session.add(bucketlistitem)
            session.commit()
            return {'message': '{} has been added to Bucketlist {}'
                               .format(item, list_id)}
        return {'message': 'Bucketlist does not exist'}


class BucketListItemEdit(Resource):
    """Resource to handle '/bucketlist/<list_id>/item/<item_id/'."""

    @login_required
    def put(self, list_id, item_id):
        """Update an existing bucketlist item."""
        bucketlistfind = session.query(
            BucketList).filter_by(list_id=list_id).first()
        if bucketlistfind:
            bucketlistitemupdate = session.query(
                BucketListItems).filter_by(item_id=item_id).first()
            if bucketlistitemupdate:
                parser.add_argument('item_name')
                args = parser.parse_args()
                bucketlistitemupdate.item_name = args['item_name']
                session.add(bucketlistitemupdate)
                session.commit()
                return {'message': 'Bucketlistitem {}  has been modified'
                                   .format(item_id)}
        return {'message': 'Bucketlist {} has not been found'
                .format(item_id)}

    @login_required
    def delete(self, list_id, item_id):
        """Delete an item form an existing bucketlist."""
        bucketlistfind = session.query(
            BucketList).filter_by(list_id=list_id).first()
        if bucketlistfind:
            bucketlistitemdelete = session.query(
                BucketListItems).filter_by(item_id=item_id).first()
            session.delete(bucketlistitemdelete)
            session.commit()
