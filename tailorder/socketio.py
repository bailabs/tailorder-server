from flask.json import loads
from flask_socketio import emit


def emit_create(order):
    res_order = order.to_json()
    res_order['lines'] = loads(res_order['lines'])
    emit('create', res_order, namespace='/', broadcast=True)


def emit_update(order, update_type, lines=None):
    res_order = order.to_json()
    res_order[update_type] = True

    if lines:
        res_order['lines'] = lines

    emit('update', res_order, namespace='/', broadcast=True)
