from flask import Blueprint
api = Blueprint('api', __name__)

from . import cancel_order, change_table, complete_order, get_orders, new_order, print_order,test_print, void_line, clear_orders, \
    uncancel_order
