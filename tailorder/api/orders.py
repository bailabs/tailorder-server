from flask import jsonify, request, current_app
from flask.json import loads, dumps

from . import api
from .. import db
from ..models import Order

@api.route('/void_line', methods=['POST'])
def void_line():
    order = _get_order_from_request()
    existing_order = _get_existing_order_by_id(order.get('id'))

    if existing_order:
        line = order.get('line')
        lines = loads(existing_order.lines)

        lines.pop(line)
        existing_order.lines = dumps(lines)

    db.session.commit()

    return jsonify(Order.to_json(existing_order)), 200


@api.route('/change_table', methods=['POST'])
def change_table():
    order = _get_order_from_request()
    existing_order = _get_existing_order_by_id(order.get('id'))

    if existing_order:
        existing_order.table_no = order.get('table')

    db.session.commit()

    return jsonify(Order.to_json(existing_order)), 200


@api.route('/cancel_order', methods=['POST'])
def cancel_order():
    order = _get_order_from_request()
    existing_order = _get_existing_order_by_id(order.get('id'))

    if existing_order:
        existing_order.is_cancelled = True

    db.session.commit()

    return jsonify(Order.to_json(existing_order)), 200


@api.route('/complete_order', methods=['POST'])
def complete_order():
    order = _get_order_from_request()
    existing_order = _get_existing_order_by_id(order.get('id'))

    if existing_order:
        existing_order.is_fulfilled = True

    db.session.commit()

    return jsonify(Order.to_json(existing_order)), 200


def _get_order_from_request():
    return loads(request.get_data(as_text=True))


def _get_existing_order_by_id(id):
    return Order.query.get(id)
