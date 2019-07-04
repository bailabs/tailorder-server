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

    order_type = existing_order.type if existing_order else order.type
    series = OrderSeries.query.filter_by(type=order_type).first()

    if existing_order:
        existing_lines = loads(existing_order.lines)
        additional_lines = loads(order.lines)

        is_usb = get_config(current_app, 'USB')
        print_item_code = get_config(current_app, 'PRINT_ITEM_CODE')

        try:
            if is_usb:
                usb_printer = get_usb(get_usb_config(current_app))

            write_additional(
                existing_order.table_no,
                additional_lines,
                usb_printer,
                print_item_code
            )
        except:
            print('Unable to print')

        existing_lines.extend(additional_lines)
        existing_order.lines = dumps(existing_lines)
        order = existing_order

        emit_update(order, 'additional', additional_lines)
    else:
        order.table_no = series.idx
        series.idx = series.idx + 1
        db.session.add(order)
        db.session.add(series)

    db.session.commit()

    if not existing_order:
        emit_create(order)

    return post_process_order(order), 201
