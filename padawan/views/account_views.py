from flask import Blueprint, redirect

from padawan.infraestructure import cookie_auth
from padawan.infraestructure.view_modifiers import response
from padawan.services import user_service
from padawan.viewmodels.account.index_viewmodel import IndexViewModel
from padawan.viewmodels.account.login_viewmodel import LoginViewModel
from padawan.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()

    if not vm.user:
        return redirect('/account/login')

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

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created'
        return vm.to_dict()

    resp = redirect('/account')

    cookie_auth.set_auth(resp, user.id)

    return resp


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = LoginViewModel()
    return vm.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = 'The account does not exist or the password is wrong.'
        return vm.to_dict()

    resp = redirect('/account')

    cookie_auth.set_auth(resp, user.id)

    return resp
