from flask import jsonify, request
from flask.json import loads

from . import api
from .. import db
from ..models import Order


@api.route('/orders/')
def get_orders():
    return jsonify([order.to_json() for order in Order.query.all()])


@api.route('/orders', methods=['POST'])
def new_order():
    order_data = request.get_data(as_text=True)
    order = Order.from_json(loads(order_data))

    db.session.add(order)
    db.session.commit()

    return jsonify(Order.to_json(order)), 201
