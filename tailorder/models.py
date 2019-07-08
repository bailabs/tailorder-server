from . import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    lines = db.Column(db.String)
    remarks = db.Column(db.String)
    table_no = db.Column(db.Integer)
    is_takeaway = db.Column(db.Boolean)
    is_fulfilled = db.Column(db.Boolean)
    is_cancelled = db.Column(db.Boolean)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __init__(self, lines, table_no, is_takeaway=False, remarks=None, type=None, items=None):
        self.lines = lines
        self.table_no = table_no
        self.is_takeaway = is_takeaway
        self.is_fulfilled = False
        self.is_cancelled = False
        self.remarks = remarks
        self.type = type

        if items:
            self.items.extend(items)

    @staticmethod
    def from_json(json_dict):
        type = json_dict.get('type')
        lines = json_dict.get('lines')
        remarks = json_dict.get('remarks')
        table_no = json_dict.get('table_no')
        is_takeaway = json_dict.get('is_takeaway')

        items = json_dict.get('items')
        items = _create_order_items(items)

        if is_takeaway:
            type = "Takeaway"
        if not type:
            type = "Dine-in"

        return Order(lines, table_no, is_takeaway, remarks, type, items=items)

    def to_json(self):
        items = list(map(lambda x: x.to_json(), self.items))
        return {
            'id': self.id,
            'type': self.type,
            # 'lines': self.lines,
            'remarks': self.remarks,
            'table_no': self.table_no,
            'is_takeaway': self.is_takeaway,
            'items': items
        }


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_name = db.Column(db.String)
    item_code = db.Column(db.String)
    qty = db.Column(db.Integer)

    def __init__(self, item_name, item_code, qty):
        self.item_name = item_name
        self.item_code = item_code
        self.qty = qty

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
            OrderItem(item.get('item_name'), item.get('item_code'), item.get('qty'))
        )

    return order_items
