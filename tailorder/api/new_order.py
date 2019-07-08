from flask import jsonify, request, current_app
from flask.json import loads, dumps

from . import api
from .. import db
from ..models import Order, OrderSeries
from ..helpers import get_config, get_usb_config, post_process_order
from ..escpos import get_usb, write_additional

from ..socketio import emit_create, emit_update


@api.route('/orders', methods=['POST'])
def new_order():
    """
    Create a new order based from the POSTed data
    :return:
    """
    order = Order.from_json(
        loads(request.get_data(as_text=True))
    )

    existing_order = Order.query.filter_by(
        table_no=order.table_no,
        is_fulfilled=False,
        is_cancelled=False
    ).first()

    if existing_order:
        additional_items = order.items

        is_usb = get_config(current_app, 'USB')
        print_item_code = get_config(current_app, 'PRINT_ITEM_CODE')

        try:
            if is_usb:
                usb_printer = get_usb(get_usb_config(current_app))

            write_additional(
                existing_order.table_no,
                additional_items,
                usb_printer,
                print_item_code
            )
        except:
            print('Unable to print')

        for item in additional_items:
            existing_order.items.append(item)

        order = existing_order
    else:
        series = _get_order_series(order.type)

        order.table_no = series.idx
        series.increment()

        db.session.add(order)
        db.session.add(series)

    db.session.commit()

    if not existing_order:
        emit_create(order)
    else:
        emit_update(order, 'additional')

    return post_process_order(order), 201


def _get_order_series(order_type):
    return OrderSeries.query.filter_by(
        type=order_type
    ).first()
