from flask import Blueprint, render_template

blueprint = Blueprint('error', __name__, template_folder='templates')


@blueprint.app_errorhandler(403)
def error_403(_):
    resp = render_template('errors/403.html')
    return resp, 403


@blueprint.app_errorhandler(404)
def error_404(_):
    resp = render_template('errors/404.html')
    return resp, 404

