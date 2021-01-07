import os
import sys

from flask import Flask

import logbook

from padawan.infraestructure.log_levels import LogLevel

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

app = Flask(__name__)


def init_logging():
    logbook.StreamHandler(sys.stdout, level=LogLevel.info).push_application()
    return logbook.Logger('App')


def register_blueprints(log: logbook.Logger):
    from padawan.views import home_views
    from padawan.views import error_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(error_views.blueprint)

    log.notice("Configuring: Blueprints registered")


def configure_app():
    log = init_logging()
    log.notice("Configuring PA·DA·WA·N Flask App: ")
    register_blueprints(log)

    return log


def run_app():
    log = configure_app()
    debug = True
    port = 5050
    log.notice(f"Starting PA·DA·WA·N app in localhost:{port} (Debug: {debug})")
    app.run(debug=debug, port=port)


if __name__ == '__main__':
    run_app()
else:
    configure_app()
