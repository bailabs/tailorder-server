from . import api
from .. import db
from ..helpers import get_existing_order_from_request, post_process_order
from ..socketio import emit_update


@api.route('/uncancel_order', methods=['POST'])
def uncancel_order():
    """
    Set the order as uncancelled
    :return:
    """
    order, request_data = get_existing_order_from_request()
    order.is_cancelled = False

    db.session.commit()

    emit_update(order, 'uncancel')

    return post_process_order(order), 200
