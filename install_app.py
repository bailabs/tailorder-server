from tailorder import create_app, db
from tailorder.models import OrderSeries

app = create_app()


def _create_order_series():
    order_types = {
        'Dine-in': 1,
        'Takeaway': 201,
        'Delivery': 301,
        'Online': 401
    }

    for type, idx in order_types.items():
        db.session.add(OrderSeries(type, id))

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        _create_order_series()
