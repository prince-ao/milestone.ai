from decouple import config


class DevConfig:
    DEBUG = True
    PORT = config("PORT")


class ProdConfig:
    ...
