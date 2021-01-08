from flask import Blueprint, redirect

from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.account.index_viewmodel import IndexViewModel
from padawan.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()

    # TODO redirect if no user
    # if not vm.user:
    #    return redirect('/account/login')

    return vm.to_dict()


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    # TODO create user en BD
    # user = user_service.create_user(vm.name, vm.email, vm.password)
    # if not user:
    #     vm.error = 'The account could not be created'
    #     return vm.to_dict()

    resp = redirect('/account')

    # TODO cookie_auth.set_auth(resp, user.id)

    return resp


