from flask import request, current_app, abort
from flask.json import loads

from . import api
from .. import db
from ..models import Order, OrderSeries, OrderItem
from ..helpers import get_config, get_usb_config, post_process_order
from ..escpos import get_usb, write_additional

from ..socketio import emit_create, emit_update


@api.route('/orders', methods=['POST'])
def new_order():
    """
    Create a new order based from the POSTed data
    :return:
    """
    order = loads(request.get_data(as_text=True))
    existing_order = _get_existing_order_by_table_no(order.get("table_no"))

    if existing_order:
        _validate_order_types(order, existing_order)

        new_items = OrderItem.list_from_json(order.get('items'))

        is_usb = get_config(current_app, 'USB')
        print_item_code = get_config(current_app, 'PRINT_ITEM_CODE')

        try:
            if is_usb:
                usb_printer = get_usb(get_usb_config(current_app))

            write_additional(
                existing_order.table_no,
                new_items,
                usb_printer,
                print_item_code
            )
        except:
            print('Unable to print')

        existing_order.items.extend(new_items)
        existing_order.is_finished = False
        order = existing_order
    else:
        order = Order.from_json(order)
        _set_table_no(order)

    db.session.add(order)
    db.session.commit()

    _emit_order(order, existing_order)

    return post_process_order(order), 201


def _get_order_series(order_type):
    return OrderSeries.query.filter_by(
        type=order_type
    ).first()


def _get_existing_order_by_table_no(table_no):
    return Order.query.filter_by(
        table_no=table_no,
        is_fulfilled=False,
        is_cancelled=False
    ).first()


def _set_table_no(order):
    if order.type != "Dine-in" and order.type != "Family":
        series = _get_order_series(order.type)
        order.table_no = series.idx
        series.increment()

        db.session.add(series)
    else:
        print(order.table_no)
        if not order.table_no:
            raise Exception('table_no is required.')


def _emit_order(order, existing_order):
    if not existing_order:
        emit_create(order)
    else:
        emit_update(order, 'additional')


def _validate_order_types(order, existing_order):
    if order.get('type') != existing_order.type:
        abort(403, description='Order exists with different order type')
