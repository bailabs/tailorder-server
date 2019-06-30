import time

from flask.json import loads
from escpos.printer import File, Usb

# Line Width
QTY_WIDTH = 6
ITEM_WIDTH = 26


def write_void(table_no, lines, usb_printer=None, print_item_code=True):
    p = usb_printer if usb_printer else File("/dev/usb/lp0")
    p.text('Table Number: {0}\n'.format(table_no))
    p.text('***VOID ITEMS***\n\n')
    p.text(line_block([
        {'text': 'Item', 'align': '<', 'width': QTY_WIDTH + ITEM_WIDTH}
    ]))

    for line in lines:
        p.text(line_block([
            {'text': line['itemName'], 'align': '<', 'width': QTY_WIDTH + ITEM_WIDTH}
        ]))

        if print_item_code:
            p.text(line_block([
                {'text': line['itemCode'], 'align': '<', 'width': QTY_WIDTH + ITEM_WIDTH}
            ]))

    p.text('\n\nPrinted on:\n')
    p.text(time.ctime())

    p.cut()


def write_additional(table_no, lines, usb_printer=None, print_item_code=True):
    p = usb_printer if usb_printer else File("/dev/usb/lp0")
    p.text('Table Number: {0}\n'.format(table_no))
    p.text('ADDITIONAL ITEMS\n\n')
    p.text(line_block([
        {'text': 'Qty', 'align': '<', 'width': QTY_WIDTH},
        {'text': 'Item', 'align': '<', 'width': ITEM_WIDTH}
    ]))

    for line in lines:
        p.text(line_block([
            {'text': line['qty'], 'align': '<', 'width': QTY_WIDTH},
            {'text': line['itemName'], 'align': '<', 'width': ITEM_WIDTH},
        ]))

        if print_item_code:
            p.text(line_block([
                {'text': '-', 'align': '<', 'width': QTY_WIDTH},
                {'text': line['itemCode'], 'align': '<', 'width': ITEM_WIDTH}
            ]))

    # Time
    p.text('\n\nPrinted on:\n')
    p.text(time.ctime())

    p.cut()


def write_order(order, usb_printer=None, print_item_code=True):
    if usb_printer:
        p = usb_printer
    else:
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
            {'text': line['itemName'], 'align': '<', 'width': ITEM_WIDTH},
        ])
        p.text(line_text)

        if print_item_code:
            item_code = line_block([
                {'text': '-', 'align': '<', 'width': QTY_WIDTH},
                {'text': line['itemCode'], 'align': '<', 'width': ITEM_WIDTH}
            ])
            p.text(item_code)

    # Remarks
    p.text('\nRemarks:\n{0}'.format(order.remarks))

    # Time
    p.text('\n\nPrinted on:\n')
    p.text(time.ctime())

    p.cut()


def get_usb(config):
    return Usb(
        config['id_vendor'],
        config['id_product'],
        0,
        config['endpoint_in'],
        config['endpoint_out']
    )


def text_block(text, width, align):
    return '{text:{align}{width}}'.format(text=text, align=align, width=width)


def line_block(contents):
    return ''.join([text_block(c['text'], c['width'], c['align']) for c in contents])
