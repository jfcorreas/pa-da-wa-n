from padawan.viewmodels.shared.viewmodelbase import ViewModelBase
from padawan.services import cms_service


class RedirectListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.redirects = cms_service.all_redirects()
