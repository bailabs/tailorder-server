from flask import request
from flask.json import loads, jsonify

from . import api
from .. import db
from ..helpers import create_order_series


@api.route('/clear_orders', methods=['POST'])
def clear_orders():
    credentials = loads(request.get_data(as_text=True))
    passkey = credentials.get('passkey')

    if passkey:
        db.drop_all()
        db.create_all()
        create_order_series(db)
        return jsonify({'is_success': 1}), 200
    else:
        raise Exception('Not allowed')
