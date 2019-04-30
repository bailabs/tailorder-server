import time

from flask.json import loads
from escpos.printer import File

# Line Width
QTY_WIDTH = 6
ITEM_WIDTH = 26


def text_block(text, width, align):
    return '{text:{align}{width}}'.format(text=text, align=align, width=width)


def line_block(contents):
    return ''.join([text_block(c['text'], c['width'], c['align']) for c in contents])


def write_order(order):
    p = File("/dev/usb/lp0")

    lines = loads(order.lines)

    # Order
    p.text('Order Id: {0}\n'.format(order.id))

    # Table Number
    p.text('Table Number: {0}\n'.format(order.table_no))

    # Take Away
    if order.is_takeaway:
        p.text('Type: TAKE AWAY\n\n')
    else:
        p.text('Type: DINE IN\n\n')

    # Headers
    header_line = line_block([
        {'text': 'Qty', 'align': '<', 'width': QTY_WIDTH},
        {'text': 'Item', 'align': '<', 'width': ITEM_WIDTH},
    ])

    p.text(header_line)

    # Lines
    for line in lines:
        line_text = line_block([
            {'text': line['qty'], 'align': '<', 'width': QTY_WIDTH},
            {'text': line['itemCode'], 'align': '<', 'width': ITEM_WIDTH},
        ])
        p.text(line_text)

    # Remarks
    p.text('\nRemarks:\n{0}'.format(order.remarks))

    # Time
    p.text('\n\nPrinted on:\n')
    p.text(time.ctime())

    p.cut()
