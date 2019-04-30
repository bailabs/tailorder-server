from . import db
from flask.json import loads


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    lines = db.Column(db.String)
    table_no = db.Column(db.Integer)
    is_takeaway = db.Column(db.Boolean)
    is_fulfilled = db.Column(db.Boolean)
    is_cancelled = db.Column(db.Boolean)

    def __init__(self, lines, table_no, is_takeaway=False):
        self.lines = lines
        self.table_no = table_no
        self.is_takeaway = is_takeaway
        self.is_fulfilled = False
        self.is_cancelled = False

    @staticmethod
    def from_json(json_dict):
        lines = json_dict.get('lines')
        table_no = json_dict.get('table_no')
        is_takeaway = json_dict.get('is_takeaway')

        return Order(lines, table_no, is_takeaway)

    def to_json(self):
        return {
            'id': self.id,
            'lines': self.lines,
            'table_no': self.table_no,
            'is_takeaway': self.is_takeaway
        }
