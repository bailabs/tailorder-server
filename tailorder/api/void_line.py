from flask.json import loads, dumps

from . import api
from .. import db

from ..helpers import get_existing_order_from_request, post_process_order
from ..socketio import emit_update


@api.route('/void_line', methods=['POST'])
def void_line():
    """
    Void lines from existing order
    :return:
    """
    existing_order, request_data = get_existing_order_from_request()

    item = existing_order.items[request_data.get('line')]
    item.is_voided = True

    existing_order.append_remarks(
        'VOID {} x {}'.format(item.qty, item.item_name)
    )

    db.session.add(existing_order)
    db.session.add(item)
    db.session.commit()

    emit_update(existing_order, 'void')

    return post_process_order(existing_order), 200
