from flask import request
from flask.ext.restful import reqparse, Resource, marshal
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import BadRequestKeyError

from sqlalchemy_paginator import Paginator
from sqlalchemy_paginator.exceptions import EmptyPage

from models import BucketList, BucketListItems
from db import session
from serializer import bucketlists, bucketlistitems


parser = reqparse.RequestParser()


def paging(fields, paginator, page):
    """
    Use imported paginator and page arguments to paginate SQLALchemy query
    sets.The fields argument it takes is used to serialize the results,
    courtesy of marshal.
    """
    try:
        return marshal(paginator.page(page).object_list, fields), 200
    except EmptyPage:
        return {'message': "Page doesn't exist"}, 404


class BucketListAll(Resource):
    """
    Resource to handle '/bucketlists/' and
    '/bucketlists/<int:page>' endpoint.
    """
    @login_required
    def get(self, page=1):
        """Retrieve all bucketlists belonging to the logged in user.
        limit specifies the maximum number of results with default set to 20.
        q specifies the term to search by through the bucketlists
        """
        try:
            limit = int(request.args['limit'])
        except BadRequestKeyError:
            limit = 20
        if limit > 100:
            limit = 100

        # try:
        #     q = request.args['q']
        # except BadRequestKeyError:
        #     q = ''

        created_by = current_user.user_id
        bucketlistget = session.query(BucketList).filter_by(
            creator=created_by)
        paginate = Paginator(bucketlistget, limit)
        page_responses = paging(bucketlists, paginate, page)
        return page_responses

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
