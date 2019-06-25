from flask import Blueprint

api = Blueprint('api', __name__)

from . import orders, get_orders, new_order, print_order, complete_order
