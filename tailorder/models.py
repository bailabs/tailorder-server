from . import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    table_no = db.Column(db.Integer)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    remarks = db.Column(db.String)
    is_fulfilled = db.Column(db.Boolean)
    is_cancelled = db.Column(db.Boolean)

    def __init__(self, table_no, order_type, items, remarks=None):
        self.table_no = table_no
        self.type = order_type # it overshadows type
        self.items = items
        self.remarks = remarks

        self.is_fulfilled = False
        self.is_cancelled = False

    @staticmethod
    def from_json(json_dict):
        type = json_dict.get('type')
        remarks = json_dict.get('remarks')
        table_no = json_dict.get('table_no')
        items = _create_order_items(
            json_dict.get('items')
        )

        return Order(table_no, type, items, remarks)

    def to_json(self):
        items = list(map(lambda x: x.to_json(), self.items))
        return {
            'id': self.id,
            'table_no': self.table_no,
            'type': self.type,
            'items': items,
            'remarks': self.remarks
        }


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_name = db.Column(db.String)
    item_code = db.Column(db.String)
    qty = db.Column(db.Integer)
    is_voided = db.Column(db.Boolean)

    def __init__(self, item_name, item_code, qty):
        self.item_name = item_name
        self.item_code = item_code
        self.qty = qty
        self.is_voided = True

    @staticmethod
    def from_json(json_dict):
        item_name = json_dict.get('item_name')
        item_code = json_dict.get('item_code')
        qty = json_dict.get('qty')

        return OrderItem(item_name, item_code, qty)

    def to_json(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'item_name': self.item_name,
            'item_code': self.item_code,
            'qty': self.qty
        }


class OrderSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    idx = db.Column(db.Integer)

    def __init__(self, type, idx):
        self.type = type
        self.idx = idx


def _create_order_items(items):
    order_items = []

    for item in items:
        order_items.append(
            OrderItem.from_json(item)
        )

    return order_items
