from . import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)

    def __init__(self, text):
        self.text = text

    @staticmethod
    def from_json(json_dict):
        text = json_dict.get('text')
        return Order(text=text)

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text
        }
