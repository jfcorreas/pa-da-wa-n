import os
import sys
import datetime

from flask import Flask
import logbook

from babel.dates import format_datetime
from babel.dates import format_timedelta

from padawan.data import db_session
from padawan.infraestructure.log_levels import LogLevel

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

app = Flask(__name__)


def init_logging():
    logbook.StreamHandler(sys.stdout, level=LogLevel.info).push_application()
    return logbook.Logger('App')


def register_blueprints(log: logbook.Logger):
    from padawan.views import home_views
    from padawan.views import account_views
    from padawan.views import admin_views
    from padawan.views import cms_views
    from padawan.views import error_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(admin_views.blueprint)
    app.register_blueprint(cms_views.blueprint)
    app.register_blueprint(error_views.blueprint)

    log.notice("Configuring: Blueprints registered")


def setup_db(log: logbook.Logger):
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'padawan.sqlite'
    )

    db_session.global_init(db_file)
    log.notice("Database Initialized")


def configure_app():
    log = init_logging()
    log.notice("Configuring PA·DA·WA·N Flask App: ")
    register_blueprints(log)
    setup_db(log)

    return log


def run_app():
    log = configure_app()
    debug = True
    port = 5050
    log.notice(f"Starting PA·DA·WA·N app in localhost:{port} (Debug: {debug})")
    app.run(debug=debug, port=port)


@app.template_filter()
def date_type(value, dateformat='medium'):
    if dateformat == 'delta':
        now = datetime.datetime.now()
        # target = datetime.datetime.strptime(value, "%y-%m-%d")
        target = value
        delta = abs(now-target)
        return format_timedelta(delta, locale='en_US')
    if dateformat == 'full':
        dateformat = "EEEE, d MMMM y 'at' HH:mm"
    elif dateformat == 'medium':
        dateformat = "dd/MM/y (HH:mm)"
    elif dateformat == 'small':
        dateformat = "dd/MM/y"
    return format_datetime(value, dateformat, locale='en_US')


if __name__ == '__main__':
    run_app()
else:
    configure_app()
