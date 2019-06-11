class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

    # Change USB settings
    USB = True
    ID_VENDOR = 0x0493
    ID_PRODUCT = 0x8760
    ENDPOINT_IN = 0x81
    ENDPOINT_OUT = 0x03
