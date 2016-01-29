from sqlalchemy import DateTime
from models import User, BucketList, BucketListItems
from db import session

from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with

users = {
    'user_id': fields.Integer,
    'username': fields.String,
    'password': fields.String
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
    'creator': fields.String,
    # 'date_created': fields.DateTime,
    # 'date_modified': fields.DateTime
}


parser = reqparse.RequestParser()


class UserRegistration(Resource):
    """Resource to handle '/auth/register/' endpoint"""

    def post(self):
        """Allow a user to register"""
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        exists = session.query(User).filter_by(username=username).first()
        if exists:
            return {'message': 'User already exists!'}
        else:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()
            return {'message': 'User {} has been successfully registered'
                               .format(username)}


class BucketListAll(Resource):
    """Resource to handle '/bucketlists/'endpoint"""

    @marshal_with(bucketlists)
    def get(self):
        """Retrieve all bucketlists belonging to the logged in user"""
        bucketlist = session.query(BucketList).all()
        return bucketlist

    @marshal_with(bucketlists)
    def post(self):
        """Create a new bucketlist"""
        parser.add_argument('list_name')
        args = parser.parse_args()
        list_name = args['list_name']

        bucketlistexist = session.query(BucketList).filter_by(
            list_name=list_name).first()
        if bucketlistexist:
            return {'message': 'Bucketlist  already exists'}
        else:
            bucketlist = BucketList(list_name=list_name)
            session.add(bucketlist)
            session.commit()
            return bucketlists, 201


class BucketListId(Resource):
    """Resource to handle '/bucketlist/<list_id>' endpoint"""

    @marshal_with(bucketlists)
    def get(self, list_id):
        """Retrieve a particular bucketlist belonging to logged in user"""
        bucketlist = session.query(BucketList).filter_by(
            list_id=list_id).first()
        if bucketlist:
            return bucketlist

        abort(404, message="Bucketlist {} does not exist".format(id))

    @marshal_with(bucketlists)
    def put(self, list_id):
        """ Modify existing bucketlist """
        bucketlistedit = session.query(
            BucketList).filter_by(list_id=list_id).first()
        if bucketlistedit:
            parser.add_argument('list_name')
            args = parser.parse_args()
            bucketlistedit.list_name = args['list_name']
            # bucketlistedit.date_modified = DateTime.now()
            session.add(bucketlistedit)
            session.commit()
            return {'message': 'Bucketlist {} has been modified'
                               .format(list_id)}
        return {'message': 'Bucketlist {} has not been found'
                .format(list_id)}

    @marshal_with(bucketlists)
    def delete(self, list_id):
        """Delete an existing bucketlist"""
        bucketlistdelete = session.query(
            BucketList).filter_by(list_id=list_id).first()
        session.delete(bucketlistdelete)
        session.commit()
        return {'message': 'Bucketlist {} has been deleted'.format(list_id)}


class BucketListItemAdd(Resource):
    """Resource to handle '/bucketlist/<list_id>/item' """

    # @marshal_with(bucketlistitems)
    def post(self, list_id):
        """Add a new item to a bucketlist"""
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
            return {'message': 'An item has been added to Bucketlist {}'
                               .format(list_id)}
            # return bucketlistitem
        return {'message': 'Bucketlist does not exist'}


class BucketListItemEdit(Resource):
    """Resource to handle '/bucketlist/<list_id>/item/<item_id/'"""

    @marshal_with(bucketlistitems)
    def put(self, list_id, item_id):
        """Update an existing bucketlist item"""
        bucketlistfind = session.query(BucketList).filter_by(list_id=list_id).first()
        if bucketlistfind:
            bucketlistitemupdate = session.query(BucketListItems).filter_by(item_id=item_id).first()
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

    @marshal_with(bucketlistitems)
    def delete(self, list_id, item_id):
        """delete an item form an existing bucketlist"""
        bucketlistfind = session.query(BucketList).filter_by(list_id=list_id).first()
        if bucketlistfind:
            bucketlistitemdelete = session.query(
                BucketListItems).filter_by(item_id=item_id).first()
            session.delete(bucketlistitemdelete)
            session.commit()
