from flask.json import loads, dumps

from . import api
from .. import db

from ..helpers import get_existing_order_from_request, post_process_order


@api.route('/void_line', methods=['POST'])
def void_line():
    order, request_data = get_existing_order_from_request()

    lines = loads(order.lines)
    lines.pop(order.get('line'))

    order.lines = dumps(lines)

    db.session.commit()

    return post_process_order(order), 200
