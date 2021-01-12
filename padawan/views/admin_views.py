from flask import Blueprint, redirect

from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.account.index_viewmodel import IndexViewModel

blueprint = Blueprint('admin', __name__, template_folder='templates')


@blueprint.route('/admin/edit_redirect', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
# TODO limit access to admin: @permissions.admin
def edit_redirect_get():
    vm = EditRedirectViewModel()
    return vm.to_dict()
