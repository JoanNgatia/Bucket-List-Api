from flask import jsonify
from app.models import User, BucketList, BucketListItems


@api.route('/bucketlists/', methods=['GET'])
def get_bucketlists():
    return jsonify({'urls': [s.get_url() for s in BucketList.query.all()]})
