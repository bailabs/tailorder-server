from flask import current_app
from .. import db
from . import api
from ..escpos import get_usb, write_order, write_order_void
from ..helpers import get_existing_order_from_request, get_config, get_usb_config, post_process_order


@api.route('/print_order', methods=['POST'])
def print_order():
    print("NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    """
    Get the existing Order based from the request
    :return:
    """
    order, request_data = get_existing_order_from_request()
    is_usb = get_config(current_app, 'USB')
    print_item_code = get_config(current_app, 'PRINT_ITEM_CODE')


    try:
        if is_usb:
            usb_printer = get_usb(get_usb_config(current_app))

        write_order(order, usb_printer, print_item_code)
    except:
        print("No printing")
    for ii in order.items:
        print(ii.is_new)
        ii.is_new = False
    db.session.commit()

    return post_process_order(order), 201

@api.route('/print_void', methods=['POST'])
def print_void():
    """
    Get the existing Order based from the request
    :return:
    """
    order, request_data = get_existing_order_from_request()
    is_usb = get_config(current_app, 'USB')
    print_item_code = get_config(current_app, 'PRINT_ITEM_CODE')

    if is_usb:
        usb_printer = get_usb(get_usb_config(current_app))

    write_order_void(order, usb_printer, print_item_code)

    return post_process_order(order), 201
