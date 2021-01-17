from flask import Blueprint

from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def home():
    vm = ViewModelBase()
    return vm.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    vm = ViewModelBase()
    return vm.to_dict()
