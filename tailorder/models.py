from . import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    lines = db.Column(db.String)
    table_no = db.Column(db.Integer)

    def __init__(self, lines, table_no):
        self.lines = lines
        self.table_no = table_no

    @staticmethod
    def from_json(json_dict):
        lines = json_dict.get('lines')
        table_no = json_dict.get('table_no')
        return Order(lines, table_no)

    def to_json(self):
        return {
            'lines': self.lines,
            'table_no': self.table_no,
        }
