import logbook
from flask import Blueprint, redirect

from padawan.services import cms_service
from padawan.infraestructure import permissions
from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.admin.editredirect_viewmodel import EditRedirectViewModel
from padawan.viewmodels.admin.publicationtlist_viewmodel import PublicationListViewModel
from padawan.viewmodels.admin.redirectlist_viewmodel import RedirectListViewModel

blueprint = Blueprint('admin', __name__, template_folder='templates')
log = logbook.Logger('cms_admin')


@blueprint.route('/admin/redirects')
@response(template_file='admin/redirects.html')
@permissions.admin
def redirects():
    vm = RedirectListViewModel()
    log.info(f"User viewing redirects: {vm.user.email}")
    return vm.to_dict()


@blueprint.route('/admin/edit_redirect', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def edit_redirect_get():
    vm = EditRedirectViewModel()
    return vm.to_dict()


@blueprint.route('/admin/edit_redirect', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def edit_redirect_post():
    vm = EditRedirectViewModel()
    vm.process_form()

    if not vm.validate():
        log.notice(f"User cannot add new redirect: {vm.user.email}. Error: {vm.error}")
        return vm.to_dict()

    cms_service.create_redirect(vm.name, vm.short_url, vm.url, vm.user.email, )
    log.notice(f"User adding new redirect: {vm.user.email}. Redirect: {vm.name} -> {vm.short_url}")

    return redirect('/admin/redirects')


@blueprint.route('/admin/publications')
@response(template_file='admin/publications.html')
@permissions.admin
def publications():
    vm = PublicationListViewModel()
    log.info(f"User viewing publications: {vm.user.email}")
    return vm.to_dict()
