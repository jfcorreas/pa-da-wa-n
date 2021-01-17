from flask import Blueprint, redirect, abort

from cms.cmsrequest_viewmodel import CmsRequestViewModel, PublicationViewModel
from view_modifiers import response

blueprint = Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/publications/<int:publication_id>')
@response(template_file='cms/publication.html')
def publication_request(publication_id):
    vm = PublicationViewModel(publication_id)
    if vm.publication:
        return vm.to_dict()

    return abort(404)


@blueprint.route('/<path:cms_url>')
@response(template_file='cms/publication.html')
def cms_request(cms_url):
    vm = CmsRequestViewModel(cms_url)

    if vm.page:
        vm = PublicationViewModel(vm.page.id)
        return vm.to_dict()

    if vm.redirect:
        return redirect(vm.redirect_url)

    return abort(404)


