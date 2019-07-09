import math

from datetime import datetime
from . import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String)
    table_no = db.Column(db.Integer)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    remarks = db.Column(db.String)
    is_fulfilled = db.Column(db.Boolean)
    is_cancelled = db.Column(db.Boolean)

    def __init__(self, table_no, order_type, items, remarks=None):
        self.table_no = table_no
        self.type = order_type  # it overshadows type
        self.items = items
        self.remarks = remarks

        self.is_fulfilled = False
        self.is_cancelled = False

        self.creation = datetime.now()

    @staticmethod
    def from_json(json_dict):
        type = json_dict.get('type')
        remarks = json_dict.get('remarks')
        table_no = json_dict.get('table_no')
        items = OrderItem.list_from_json(
            json_dict.get('items')
        )

        return Order(table_no, type, items, remarks)

    def to_json(self):
        items = list(map(lambda x: x.to_json(), self.items))
        return {
            'id': self.id,
            'creation': self.get_creation(),
            'type': self.type,
            'table_no': self.table_no,
            'items': items,
            'remarks': self.remarks,
            'is_fulfilled': self.is_fulfilled,
            'is_cancelled': self.is_cancelled
        }

    def get_creation(self):
        return math.floor(datetime.timestamp(self.creation) * 1000)

    def append_remarks(self, remarks):
        if self.remarks:
            self.remarks = '{}\n{}'.format(self.remarks, remarks)
        else:
            self.remarks = remarks


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False)
    parent = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_name = db.Column(db.String)
    item_code = db.Column(db.String)
    qty = db.Column(db.Integer)
    is_voided = db.Column(db.Boolean)
    
    def __init__(self, item_name, item_code, qty, creation=None):
        self.item_name = item_name
        self.item_code = item_code
        self.qty = qty
        self.is_voided = False

        self.creation = creation or datetime.now()

    @staticmethod
    def from_json(json_dict, creation):
        item_name = json_dict.get('item_name')
        item_code = json_dict.get('item_code')
        qty = json_dict.get('qty')

        return OrderItem(item_name, item_code, qty, creation)

    @staticmethod
    def list_from_json(items):
        creation = datetime.now()
        return [OrderItem.from_json(item, creation) for item in items]

    @staticmethod
    def clone(item):
        return OrderItem(
            item.item_name,
            item.item_code,
            item.qty,
            item.creation
        )

    def to_json(self):
        return {
            'id': self.id,
            'creation': self.get_creation(),
            'parent': self.parent,
            'item_name': self.item_name,
            'item_code': self.item_code,
            'qty': self.qty,
            'is_voided': self.is_voided
        }

    def get_creation(self):
        return math.floor(datetime.timestamp(self.creation) * 1000)


class OrderSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    idx = db.Column(db.Integer)

    def __init__(self, type, idx):
        self.type = type
        self.idx = idx

    def increment(self):
        self.idx = self.idx + 1
