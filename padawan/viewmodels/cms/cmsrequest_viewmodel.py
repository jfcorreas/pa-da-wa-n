from flask import request

import cms_service
from padawan.viewmodels.shared.viewmodelbase import ViewModelBase


class CmsRequestViewModel(ViewModelBase):
    def __init__(self, cms_url):
        super().__init__()

        self.cms_url = cms_url
        self.page = cms_service.get_publication_by_url(self.cms_url)
        self.redirect = cms_service.get_redirect(self.cms_url)
        self.redirect_url = None
        if self.redirect:
            dest = self.redirect.url
            query = request.query_string
            if query:
                query = query.decode('utf-8')
                dest = f'{dest}?{query}'
            self.redirect_url = dest


class PublicationViewModel(ViewModelBase):
    def __init__(self, publication_id):
        super().__init__()

        self.publication_id = publication_id
        self.publication = cms_service.find_publication_by_id(self.publication_id)
        self.html = self.publication.content
