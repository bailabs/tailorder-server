from flask import jsonify

from . import api
from ..models import Order


@api.route('/orders/')
def get_orders():
    """
    Filters order which are not fulfilled and not cancelled
    :return:
    """
    return jsonify(
        [order.to_json() for order in Order.query.filter_by(is_fulfilled=False, is_cancelled=False)]
    )


@api.route('/all_orders/')
def get_all_orders():
    """
    Get all orders
    :return:
    """
    return jsonify(
        [order.to_json() for order in Order.query.all()]
    )
