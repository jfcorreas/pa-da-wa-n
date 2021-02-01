import logbook
from flask import Blueprint, redirect, abort

from padawan.services import cms_service
from padawan.infraestructure import permissions
from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.admin.editredirect_viewmodel import EditRedirectViewModel
from padawan.viewmodels.admin.publicationtlist_viewmodel import PublicationListViewModel
from padawan.viewmodels.admin.editpublication_viewmodel import EditPublicationViewModel
from padawan.viewmodels.admin.redirectlist_viewmodel import RedirectListViewModel
from padawan.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = Blueprint('admin', __name__, template_folder='templates')
log = logbook.Logger('cms_admin')


@blueprint.route('/admin')
@response(template_file='admin/index.html')
@permissions.admin
def admin():
    vm = ViewModelBase()
    return vm.to_dict()


@blueprint.route('/admin/redirects')
@response(template_file='admin/redirects.html')
@permissions.admin
def redirects():
    vm = RedirectListViewModel()
    log.info(f"User viewing redirects: {vm.user.email}")
    return vm.to_dict()


@blueprint.route('/admin/add_redirect', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def add_redirect_get():
    vm = EditRedirectViewModel()
    return vm.to_dict()


@blueprint.route('/admin/add_redirect', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def add_redirect_post():
    vm = EditRedirectViewModel()
    vm.process_form()

    if not vm.validate():
        log.notice(f"User cannot add new redirect: {vm.user.email}. Error: {vm.error}")
        return vm.to_dict()

    cms_service.create_redirect(vm.name, vm.short_url, vm.url, vm.user.email, )
    log.notice(f"User adding new redirect: {vm.user.email}. Redirect: {vm.name} -> {vm.short_url}")

    return redirect('/admin/redirects')


@blueprint.route('/admin/edit_redirect/<int:redirect_id>', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def edit_redirect_get(redirect_id: int):
    vm = EditRedirectViewModel(redirect_id)
    if not vm.redirect:
        return abort(404)
    return vm.to_dict()


@blueprint.route('/admin/edit_redirect/<int:redirect_id>', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
@permissions.admin
def edit_redirect_post(redirect_id: int):
    vm = EditRedirectViewModel(redirect_id)
    vm.process_form()

    if not vm.validate():
        log.notice(f"User cannot edit redirect: {vm.user.email}. Error: {vm.error}")
        return vm.to_dict()

    cms_service.update_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)
    log.notice(f"User editing redirect: {vm.user.email}. Redirect: {vm.name} -> {vm.short_url}")

    return redirect('/admin/redirects')


@blueprint.route('/admin/publications')
@response(template_file='admin/publications.html')
@permissions.admin
def publications():
    vm = PublicationListViewModel()
    log.info(f"User viewing publications: {vm.user.email}")
    return vm.to_dict()


@blueprint.route('/admin/add_publication', methods=['GET'])
@response(template_file='admin/edit_publication.html')
@permissions.admin
def add_publication_get():
    vm = EditPublicationViewModel()
    return vm.to_dict()


@blueprint.route('/admin/add_publication', methods=['POST'])
@response(template_file='admin/edit_publication.html')
@permissions.admin
def add_publication_post():
    vm = EditPublicationViewModel()
    vm.process_form()

    if not vm.validate():
        log.notice(f"User cannot add new publication: {vm.user.email}. Error: {vm.error}")
        return vm.to_dict()

    cms_service.create_publication(vm.title, vm.short_url, vm.content, vm.is_snippet, vm.user.email)
    log.notice(f"User adding new publication: {vm.user.email}. Publication: {vm.title}")

    return redirect('/admin/publications')


@blueprint.route('/admin/edit_publication/<int:publication_id>', methods=['GET'])
@response(template_file='admin/edit_publication.html')
@permissions.admin
def edit_publication_get(publication_id: int):
    vm = EditPublicationViewModel(publication_id)
    if not vm.publication:
        return abort(404)
    return vm.to_dict()


@blueprint.route('/admin/edit_publication/<int:publication_id>', methods=['POST'])
@response(template_file='admin/edit_publication.html')
@permissions.admin
def edit_publication_post(publication_id: int):
    vm = EditPublicationViewModel(publication_id)
    vm.process_form()

    if not vm.validate():
        log.notice(f"User cannot edit publication: {vm.user.email}. Error: {vm.error}")
        return vm.to_dict()

    cms_service.update_publication(vm.publication_id, vm.title, vm.short_url, vm.content,
                                   vm.is_snippet, vm.user.email)
    log.notice(f"User editing publication: {vm.user.email}. Publication: {vm.title}")

    return redirect('/admin/publications')
