from app import create_app
from app.config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)

    app.run(port=5002)
