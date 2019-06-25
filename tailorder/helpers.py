def get_config(app, key):
    return app.config.get(key)


def get_usb_config(app):
    return {
        'id_vendor': app.config.get('ID_VENDOR'),
        'id_product': app.config.get('ID_PRODUCT'),
        'endpoint_in': app.config.get('ENDPOINT_IN'),
        'endpoint_out': app.config.get('ENDPOINT_OUT')
    }
