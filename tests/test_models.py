from tailorder.models import Order


def test_new_order_dine_in():
    order = Order('test', 1, type='Dine-In')
    assert order.lines == 'test'
    assert order.table_no == 1
    assert order.type == 'Dine-In'


def test_new_order_takeaway():
    order = Order('test', 2, type='Takeaway')
    assert order.lines == 'test'
    assert order.table_no == 2
    assert order.type == 'Takeaway'
    assert order.type != 'Dine-In'


def test_order_to_json():
    order = Order('test', 2, type='Takeaway')
    order_json = order.to_json()
    assert order_json['type'] == 'Takeaway'
    assert order_json['lines'] == 'test'
    assert not order_json['remarks']
    assert order_json['table_no'] == 2
    assert not order_json['is_takeaway']


def test_order_from_json():
    order = Order.from_json({
        'type': 'Online',
        'lines': 'test',
        'table_no': 1,
        'is_takeaway': False
    })
    assert order.lines == 'test'
    assert order.type == 'Online'
    assert order.table_no == 1
    assert not order.is_takeaway
