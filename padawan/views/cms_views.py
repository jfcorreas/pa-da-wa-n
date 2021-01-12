from flask import Blueprint, redirect, abort

from cms.cmsrequest_viewmodel import CmsRequestViewModel

blueprint = Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/<path:cms_url>')
def cms_request(cms_url):
    vm = CmsRequestViewModel(cms_url)

    if vm.page:
        return vm.to_dict()

    if vm.redirect:
        return redirect(vm.redirect_url)

    return abort(404)


