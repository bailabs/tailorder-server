from . import api
from .. import db
from ..helpers import get_existing_order_from_request, post_process_order


@api.route('/change_table', methods=['POST'])
def change_table():
    """
    Set the table number to what was sent
    :return:
    """
    order, request_data = get_existing_order_from_request()
    order.table_no = request_data.get('table')

    db.session.commit()

    return post_process_order(order), 200
