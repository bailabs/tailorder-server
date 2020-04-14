import arabic_reshaper
import serial
from . import api
from ..helpers import post_process_order,get_existing_order_from_request

from flask import request
from escpos import printer
from bidi.algorithm import get_display
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor
from flask.json import loads

@api.route('/print_bill', methods=['POST'])
def print_bill():
    print("asdad")
    receipt_from_tailpos = loads(request.get_data(as_text=True))
    for_printing = receipt_from_tailpos['data']

    print(for_printing)

    #print(loads(for_receipt['data']['mop'])[0]['translation_text'])
    #reshaped_text = arabic_reshaper.reshape(loads(for_receipt['data']['mop'])[0]['translation_text'])
    #rev_text = reshaped_text[::-1]  # slice backwards

    # Some variable
    port_serial = "/dev/rfcomm4"

    bluetoothSerial = serial.Serial(port_serial, baudrate=115200, timeout=1)
    print(bluetoothSerial)
    fontPath = "/usr/share/fonts/opentype/fonts-hosny-thabit/Thabit.ttf"

    tmpImage = 'test1.png'
    printWidth = 250

    # Get the characters in order
    textReshaped = arabic_reshaper.reshape(for_printing['company'])
    textDisplay = get_display(textReshaped)

    # PIL can't do this correctly, need to use 'wand'.
    # Based on
    # https://stackoverflow.com/questions/5732408/printing-bidi-text-to-an-image

    im = wImage(width=printWidth, height=36, background=wColor('#ffffff'))

    draw = wDrawing()
    draw.text_alignment = 'center';
    draw.text_antialias = False
    draw.text_encoding = 'utf-8'
    draw.text_kerning = 0.0
    draw.font = fontPath
    draw.font_size = 36
    draw.text(printWidth, 22, textDisplay)
    draw(im)
    im.save(filename=tmpImage)

    # Print an image with your printer library
    printertest = printer.File(port_serial)
    printertest.set(align="right")
    printertest.image(tmpImage)
    printertest.cut()
    print("SAMOKA GYUD Oi")
    bluetoothSerial.close()
    return {}

@api.route('/print_receipt', methods=['POST'])
def print_receipt():

    receipt_from_tailpos = loads(request.get_data(as_text=True))
    for_printing = receipt_from_tailpos['data']
    print(for_printing)

    port_serial = "/dev/rfcomm0"

    bluetoothSerial = serial.Serial(port_serial, baudrate=115200, timeout=1)
    #fontPath = "/home/jiloysss/Documents/spiceco/aljazeera-font/FontAljazeeraColor-lzzD.ttf"
    fontPath = "/home/pi/FontAljazeeraColor-lzzD.ttf"
    tmpImage = 'receipt.png'
    #printWidth = 375
    printWidth = 570

    height = 600
    draw = wDrawing()
    draw.font = fontPath

    #COMPANY ==============
    draw.font_size = 34

    draw.text(x=180,y=75,body=for_printing['company'])


    #DATE ==================
    split_date = for_printing['date'].split()
    draw.font_size = 26
    draw.text(x=5,y=110,body=split_date[0])
    draw.text(x=260,y=110,body=split_date[1])

    #ORDER TYPE ==============
    draw.font_size = 26
    draw.text(x=5,y=145,body="Order Type: " +  for_printing['ordertype'])
    y_value = 145
    #HEADER ==========

    if for_printing['header']:
        header_value = 160
        for x in for_printing['header'].split("\n"):
            y_value = y_value + 35
            header_value = header_value + 25
            draw.text_alignment = "center"
            draw.text(x=180,y=header_value,body=x)

    draw.text_alignment = "undefined"

    draw.text(x=5,y=y_value + 35 ,body="=====================================")

    #ITEM PURCHASES
    y_value = y_value + 30
    for idx,i in enumerate(for_printing['lines']):
        if idx != 0:
            height += 35
        draw.gravity = "north_east"
        draw.text(x=5,y=y_value + 10,body=format(float(i['qty'] * i['price']), '.2f'))
        draw.gravity = "forget"

        if len(i['item_name']) > 22:
            quotient = len(i['item_name']) / 22
            for xxx in range(0,int(quotient)):
                if idx != 0:
                    height += 35
                y_value = y_value + 35
                draw.text(x=5,y=y_value,body=i['item_name'][xxx * 22: (xxx+1) * 22])
            translation_text = ""
            if i['translation_text']:
                textReshaped = arabic_reshaper.reshape(i['translation_text'])
                textDisplay = get_display(textReshaped)
                translation_text = "(" + textReshaped + ")"
            y_value = y_value + 35
            draw.text(x=5,y=y_value,body=i['item_name'][(int(quotient)*22): len(i['item_name'])] + translation_text )

        else:
            translation_text = ""
            if i['translation_text']:
                textReshaped = arabic_reshaper.reshape(i['translation_text'])
                textDisplay = get_display(textReshaped)
                translation_text = "(" + textReshaped + ")"
            y_value = y_value + 35
            draw.text(x=5,y=y_value,body=i['item_name'] )
            y_value = y_value + 35
            draw.text(x=5,y=y_value,body= translation_text)


    draw.text(x=5,y=y_value+35,body="=====================================")

    y_value = y_value + 35

    #SUBTOTAL
    draw.text(x=5,y=y_value + 35,body="Subtotal")
    draw.gravity = "north_east"
    draw.text(x=5,y=y_value + 5,body=for_printing['subtotal'])
    draw.gravity = "forget"

    y_value = y_value + 35

    #DISCOUNT

    draw.text(x=5,y=y_value + 35,body="Discount")
    draw.gravity = "north_east"
    draw.text(x=5,y=y_value + 5,body=for_printing['discount'])
    draw.gravity = "forget"

    #TAXES VALUES
    if len(for_printing['taxesvalues']) > 0:
        y_value = y_value + 35
        for idx,iii in enumerate(for_printing['taxesvalues']):
            if idx != 0:
                height += 35
            y_value = y_value + 35

            draw.text(x=5,y=y_value,body=iii['name'])
            draw.gravity = "north_east"
            draw.text(x=5,y=y_value - 25,body=str(format(round(float(iii['totalAmount']),2), '.2f')))
            draw.gravity = "forget"

    #MODE OF PAYMENT
    for idx, ii in enumerate(loads(for_printing['mop'])):
        if idx != 0:
            height += 35
        y_value = y_value + 70
        type = ii['type']

        if ii['translation_text']:
            textReshaped = arabic_reshaper.reshape(ii['translation_text'])
            textDisplay = get_display(textReshaped)
            type += "(" + textReshaped + ")"

        draw.text(x=5,y=y_value,body=type)
        draw.gravity = "north_east"
        draw.text(x=5,y=y_value - 25,body=str(format(float(ii['amount']), '.2f')))
        draw.gravity = "forget"



    #TOTAL AMOUNT

    draw.text(x=5,y=y_value + 35,body="Total Amount")
    draw.gravity = "north_east"
    draw.text(x=5,y=y_value + 5,body=str(format(float(for_printing['total_amount']), '.2f')))
    draw.gravity = "forget"

    #CHANGE

    draw.text(x=5,y=y_value + 70,body="Change")
    draw.gravity = "north_east"
    draw.text(x=5,y=y_value + 43,body=str(format(float(for_printing['change']), '.2f')))
    draw.gravity = "forget"

    draw.text(x=5,y=y_value+105,body="=====================================")

    #FOOTER ==========

    if for_printing['footer']:
        header_value = y_value+105
        for x in for_printing['footer'].split("\n"):
            y_value = y_value + 35
            header_value = header_value + 25
            draw.text_alignment = "center"
            draw.text(x=180,y=header_value,body=x)

    im = wImage(width=printWidth, height=height, background=wColor('#ffffff'))
    draw(im)

    im.save(filename=tmpImage)

    # Print an image with your printer library
    printertest = printer.File(port_serial)
    printertest.set(align="left")
    printertest.image(tmpImage)
    printertest.cut()
    print("SAMOKA GYUD Oi")
    bluetoothSerial.close()
    return {}


