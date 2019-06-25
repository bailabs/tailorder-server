from flask import jsonify, request, current_app
from flask.json import loads, dumps

from . import api
from .. import db
from ..models import Order
from ..escpos import write_order, get_usb
from ..helpers import get_usb_config


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


@api.route('/print_order', methods=['POST'])
def print_order():
    order = _get_order_from_request()
    existing_order = _get_existing_order_by_id(order.get('id'))

    if existing_order:
        is_usb = current_app.config.get('USB')
        print_item_code = current_app.config.get('PRINT_ITEM_CODE')

        if is_usb:
            usb_printer = get_usb(get_usb_config(current_app))

        write_order(existing_order, usb_printer, print_item_code)

    return jsonify(Order.to_json(existing_order)), 200


def _get_order_from_request():
    return loads(request.get_data(as_text=True))


def _get_existing_order_by_id(id):
    return Order.query.get(id)
