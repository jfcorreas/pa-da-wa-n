import cms_service
from padawan.viewmodels.shared.viewmodelbase import ViewModelBase


class EditRedirectViewModel(ViewModelBase):
    def __init__(self, redirect_id: int = 0):
        super().__init__()

        self.name = ''
        self.short_url = ''
        self.url = ''
        self.redirect = None
        self.redirect_id = redirect_id

        if self.redirect_id:
            self.redirect_id = cms_service.find_redirect_by_id(self.redirect_id)

        if self.redirect:
            self.name = self.redirect.name
            self.url = self.url.name
            self.short_url = self.url.name

        self.error = None

    def process_form(self):
        d = self.request_dict
        self.name = d.get('name', '').strip()
        self.url = d.get('url', '').strip().lower()
        self.short_url = d.get('short_url', '').strip().lower()

    def validate(self) -> bool:
        if not self.name or not self.name.strip():
            self.error = 'You must specify a name'
            return False

        if not self.url or not self.url.strip():
            self.error = 'You must specify an URL'
            return False

        if not self.short_url or not self.short_url.strip():
            self.error = 'You must specify a sort URL'
            return False

        if self.redirect_id and not self.redirect:
            self.error = f"The redirect with ID {self.redirect_id} doesn't exists"
            return False

        if not self.redirect_id and cms_service.get_redirect(self.short_url):
            self.error = f"The redirect with url /{self.short_url} already exists"
            return False

        return True
