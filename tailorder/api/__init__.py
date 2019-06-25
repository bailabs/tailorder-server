from flask import Blueprint

api = Blueprint('api', __name__)

from . import orders
from . import get_orders
from . import new_order
from . import print_order
