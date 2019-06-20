from tailorder import create_app, db
from tailorder.models import OrderSeries

ORDER_TYPES = {
    'Dine-in': 1,
    'Takeaway': 201,
    'Delivery': 301,
    'Online': 401
}

app = create_app()

with app.app_context():
    print("[TailOrder] Initializing database")

    db.create_all()

    for type, idx in ORDER_TYPES.items():
        db.session.add(
            OrderSeries(type, idx)
        )

    db.session.commit()
