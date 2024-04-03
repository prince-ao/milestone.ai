from decouple import config


class DevConfig:
    DEBUG = True
    PORT = config("PORT")
    SECRET_KEY = config("SECRET_KEY")


class ProdConfig:
    ...
