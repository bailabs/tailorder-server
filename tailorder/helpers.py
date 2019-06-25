from flask import request
from flask.json import loads, jsonify

from .models import Order


def get_config(app, key):
    return app.config.get(key)


def get_usb_config(app):
    return {
        'id_vendor': app.config.get('ID_VENDOR'),
        'id_product': app.config.get('ID_PRODUCT'),
        'endpoint_in': app.config.get('ENDPOINT_IN'),
        'endpoint_out': app.config.get('ENDPOINT_OUT')
    }


def get_existing_order_from_request():
    order = loads(request.get_data(as_text=True))
    return Order.query.get(
        order.get('id')
    )


def post_process_order(order):
    return jsonify(Order.to_json(order))
