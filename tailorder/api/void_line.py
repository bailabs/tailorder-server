from flask.json import loads, dumps

from . import api
from .. import db

from ..helpers import get_existing_order_from_request, post_process_order


@api.route('/void_line', methods=['POST'])
def void_line():
    order, request_data = get_existing_order_from_request()

    lines = loads(order.lines)

    voided_line = (lines.pop(request_data.get('line')))
    qty = voided_line['qty']
    item_name = voided_line['itemName']

    order.lines = dumps(lines)
    order.remarks = order.remarks + '\nVOID {0} x {1}'.format(qty, item_name)

    db.session.commit()

    return post_process_order(order), 200
