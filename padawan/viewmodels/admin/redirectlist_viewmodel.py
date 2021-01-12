from padawan.viewmodels.shared.viewmodelbase import ViewModelBase
import cms_service


class RedirectListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.redirects = cms_service.all_redirects()
