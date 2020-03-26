import arabic_reshaper
import serial
from . import api
from ..helpers import post_process_order,get_existing_order_from_request

from escpos import printer
from bidi.algorithm import get_display
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor

from escpos.printer import Network


@api.route('/test_print', methods=['POST'])
def test_print():
    print("TEST")

    kitchen = Network("192.168.1.100") #Printer IP Address
    kitchen.text("بعض النصوص من جوجل ترجمة\n")
    kitchen.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    kitchen.cut()
    order, request_data = get_existing_order_from_request()

    return post_process_order(order), 201
