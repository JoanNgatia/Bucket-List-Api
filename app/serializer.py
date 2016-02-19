"""
    This file defines the serializing method to
    be used by the marshal function.
"""

from flask_restful import fields

bucketlistitems = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'done': fields.Boolean,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

bucketlists = {
    'id': fields.Integer(attribute='list_id'),
    'creator': fields.String,
    'list_name': fields.String,
    'items': fields.Nested(bucketlistitems),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}
