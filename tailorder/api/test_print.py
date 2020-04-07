import arabic_reshaper
import serial
from . import api
from ..helpers import post_process_order,get_existing_order_from_request

from escpos import printer
from bidi.algorithm import get_display
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor


@api.route('/test_print', methods=['POST'])
def test_print():
    print("TEST")
    # Some variables
    bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)

    #fontPath = "/usr/share/fonts/opentype/fonts-hosny-thabit/Thabit.ttf"
    fontPath = "/usr/share/fonts/opentype/linux-libertine/LinBiolinum_RI.otf"
    textUtf8 = u"بعض النصوص من جوجل ترجمة"
    tmpImage = 'my-text.png'
    printFile = "/dev/rfcomm0"
    printWidth = 250

    # Get the characters in order
    textReshaped = arabic_reshaper.reshape(textUtf8)
    textDisplay = get_display(textReshaped)

    # PIL can't do this correctly, need to use 'wand'.
    # Based on
    # https://stackoverflow.com/questions/5732408/printing-bidi-text-to-an-image
    im = wImage(width=printWidth, height=36, background=wColor('#ffffff'))
    draw = wDrawing()
    draw.text_alignment = 'right';
    draw.text_antialias = False
    draw.text_encoding = 'utf-8'
    draw.text_kerning = 0.0
    draw.font = fontPath
    draw.font_size = 36
    draw.text(printWidth, 22, textDisplay)
    draw(im)
    im.save(filename=tmpImage)

    # Print an image with your printer library
    printertest = printer.File(printFile)
    printertest.set(align="right")
    printertest.image(tmpImage)
    printertest.cut()
    order, request_data = get_existing_order_from_request()

    return post_process_order(order), 201
