from tailorder import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("Initializing Socket.IO")
    socketio.run(app, host='0.0.0.0')
