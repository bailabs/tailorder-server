from . import api
from .. import db
from ..helpers import get_existing_order_from_request, post_process_order


@api.route('/cancel_order', methods=['POST'])
def cancel_order():
    """
    Set the order as cancelled
    :return:
    """
    order = get_existing_order_from_request()
    order.is_cancelled = True

    db.session.commit()

    return post_process_order(order), 200
