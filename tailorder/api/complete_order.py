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

@api.route('/done_order', methods=['POST'])
def done_order():
    """
    Set the order as finished
    :return:
    """
    order, request_data = get_existing_order_from_request()
    order.is_finished = True

    print("ORDEEEEEEEEEER")
    print(order.items)
    for item in order.items:
        item.is_done = True
    db.session.commit()

    emit_update(order, 'finish')

    return post_process_order(order), 200

@api.route('/done_order1', methods=['POST'])
def done_order1():
    """
    Void lines from existing order
    :return:
    """
    existing_order, request_data = get_existing_order_from_request()
    get_index = existing_order.getindex(request_data.get('line_id'))
    item = existing_order.items[get_index]
    item.is_done = True



    db.session.add(existing_order)
    db.session.add(item)
    db.session.commit()

    emit_update(existing_order, 'done')

    return post_process_order(existing_order), 200