from tailorder import create_app, db, socketio
from tailorder.models import OrderSeries

ORDER_TYPES = {
    'Dine-in': 1,
    'Takeaway': 201,
    'Delivery': 301,
    'Online': 401
}

app = create_app()

if __name__ == '__main__':

    with app.app_context():
        print("[TailOrder] Initializing database")
        db.drop_all()
        db.create_all()

        for type, idx in ORDER_TYPES.items():
            db.session.add(
                OrderSeries(type, idx)
            )

        db.session.commit()

    socketio.run(app, host='0.0.0.0')
