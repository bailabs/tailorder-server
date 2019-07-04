from . import api
from .. import db
from ..helpers import get_existing_order_from_request, post_process_order
from ..socketio import emit_update


@api.route('/complete_order', methods=['POST'])
def complete_order():
    """
    Set the order as fulfilled
    :return:
    """
    order, request_data = get_existing_order_from_request()
    order.is_fulfilled = True

    db.session.commit()

    emit_update(order, 'fulfill')

    return post_process_order(order), 200
