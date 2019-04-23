from tailorder import create_app, db

app = create_app()

with app.app_context():
    print("[TailOrder] Initializing database")
    db.create_all()
