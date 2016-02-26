"""
This module uses Flask-Restful to gives the resources
access to HTTP methods.
"""
from flask import request
from flask_restful import reqparse, Resource, marshal
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import BadRequestKeyError

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_paginator import Paginator
from sqlalchemy_paginator.exceptions import EmptyPage

from models import BucketList, BucketListItems
from database import session
from serializer import bucketlists


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


def _get_bucketlist(list_id):
    """Check that the bucketlist belongs to current user."""
    created_by = current_user.user_id
    bucketlist = session.query(BucketList).filter_by(
        list_id=list_id, creator=created_by).first()
    if not bucketlist:
        raise NoResultFound
    return bucketlist


def _get_bucketlist_item(item_id, list_id):
    """Check that a bucketlist item exists."""
    bucketlistitem = session.query(
        BucketListItems).filter_by(item_id=item_id, bucket_id=list_id).first()
    if not bucketlistitem:
        raise NoResultFound
    return bucketlistitem


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

        q = request.args.get('q', type=str)

        created_by = current_user.user_id
        if created_by:
            if q:
                bucketlistget = session.query(BucketList).filter_by(
                    creator=created_by).filter(
                        BucketList.list_name.contains(q))
            else:
                bucketlistget = session.query(BucketList).filter_by(
                    creator=created_by)
            paginate = Paginator(bucketlistget, limit)
            page_responses = paging(bucketlists, paginate, page)
            return page_responses
        return {'message': 'Please login to view your bucketlists'}, 401

    @login_required
    def post(self):
        """Create a new bucketlist."""
        parser.add_argument('list_name',
                            help='List name cannot be blank')
        arg = parser.parse_args()
        if arg['list_name']:
            list_name = arg['list_name']
        else:
            return {'message': 'Invalid value passed.'}
        created_by = current_user.user_id
        bucketlistexist = session.query(BucketList).filter_by(
            list_name=list_name, creator=created_by).first()
        if bucketlistexist:
            return {'message': 'Bucketlist  already exists'}, 400
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
        try:
            bucketlist = _get_bucketlist(list_id)
            return marshal(bucketlist, bucketlists), 200
        except NoResultFound:
            return {'message': 'Bucketlist {} not found'.format(list_id)}, 404

    @login_required
    def put(self, list_id):
        """Modify existing bucketlist."""
        try:
            bucketlist = _get_bucketlist(list_id)
            parser.add_argument('list_name')
            arg = parser.parse_args()
            if arg['list_name']:
                bucketlist.list_name = arg['list_name']
            else:
                return {'message': 'Invalid value passed.'}
            session.add(bucketlist)
            session.commit()
            return {'message': 'Bucketlist {} has been modified'
                               .format(list_id)}, 202
        except NoResultFound:
            return {'message': 'Bucketlist {} has not been found'
                               .format(list_id)}, 404

    @login_required
    def delete(self, list_id):
        """Delete an existing bucketlist."""
        try:
            bucketlist = _get_bucketlist(list_id)
            session.delete(bucketlist)
            session.commit()
            return {'message': 'Bucketlist {} has been deleted'
                               .format(list_id)}, 200
        except NoResultFound:
            return {'message': 'Bucketlist {} has not been found'
                               .format(list_id)}, 404


class BucketListItemAdd(Resource):
    """Resource to handle '/bucketlists/<list_id>/items/'."""

    @login_required
    def post(self, list_id):
        """Add a new item to a bucketlist."""
        try:
            bucketlist = _get_bucketlist(list_id)
            parser.add_argument('item_name')
            arg = parser.parse_args()
            if arg['item_name']:
                item = arg['item_name']
            else:
                return {'message': 'Invalid value passed.'}
            bucketlistitem = BucketListItems(
                item_name=item, bucket_id=bucketlist.list_id)
            session.add(bucketlistitem)
            session.commit()
            return {'message': '{0} has been added to Bucketlist {1}'
                               .format(item, list_id)}, 201
        except NoResultFound:
            return {'message': 'Bucketlist does not exist'
                               .format(list_id)}, 404


class BucketListItemEdit(Resource):
    """Resource to handle '/bucketlist/<list_id>/item/<item_id/'."""

    @login_required
    def put(self, list_id, item_id):
        """Update an existing bucketlist item."""
        try:
            bucketlistitem = _get_bucketlist_item(item_id, list_id)
            parser.add_argument('item_name')
            parser.add_argument('done')
            arg = parser.parse_args()
            if arg['item_name']:
                bucketlistitem.item_name = arg['item_name']
            if arg['done']:
                bucketlistitem.done = arg['done']
            if not arg['item_name'] and not arg['done']:
                return {'message': 'Invalid value passed.'}
            session.add(bucketlistitem)
            session.commit()
            return {'message': 'Bucketlistitem {}  has been modified'
                               .format(item_id)}, 202
        except NoResultFound:
            return {'message': 'Bucketlist {} has not been found'
                               .format(list_id)}, 404

    @login_required
    def delete(self, list_id, item_id):
        """Delete an item form an existing bucketlist."""
        bucketlist = _get_bucketlist(list_id)
        if bucketlist:
            bucketlistitem = _get_bucketlist_item(item_id, list_id)
            session.delete(bucketlistitem)
            session.commit()
            return {'message': 'BucketlistItem {} has been deleted'
                               .format(item_id)}, 204
        return {'message': 'Bucketlistitem {} could not be found'
                           .format(item_id)}, 404
