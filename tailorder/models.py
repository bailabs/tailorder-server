from . import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    lines = db.Column(db.String)
    remarks = db.Column(db.String)
    table_no = db.Column(db.Integer)
    is_takeaway = db.Column(db.Boolean)
    is_fulfilled = db.Column(db.Boolean)
    is_cancelled = db.Column(db.Boolean)

    def __init__(self, lines, table_no, is_takeaway=False, remarks=None, type=None):
        self.lines = lines
        self.table_no = table_no
        self.is_takeaway = is_takeaway
        self.is_fulfilled = False
        self.is_cancelled = False
        self.remarks = remarks
        self.type = type

    @staticmethod
    def from_json(json_dict):
        type = json_dict.get('type')
        lines = json_dict.get('lines')
        remarks = json_dict.get('remarks')
        table_no = json_dict.get('table_no')
        is_takeaway = json_dict.get('is_takeaway')
        return Order(lines, table_no, is_takeaway, remarks, type)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'lines': self.lines,
            'remarks': self.remarks,
            'table_no': self.table_no,
            'is_takeaway': self.is_takeaway,
        }


class OrderSeries(db.Model):
    __table__ = 'order_series'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    last_idx = db.Column(db.Integer)

    def __init__(self, type):
        self.type = type
        self.last_idx = 0
