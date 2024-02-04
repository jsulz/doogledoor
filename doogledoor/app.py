import os
from flask import Flask
from . import doogledoor


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(doogledoor.doog)

    return app
