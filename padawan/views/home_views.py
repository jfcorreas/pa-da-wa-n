from flask import Blueprint, render_template

from padawan.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
def home():
    vm = ViewModelBase()
    return render_template('home/index.html', **vm.to_dict())
