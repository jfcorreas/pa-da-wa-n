from padawan.viewmodels.shared.viewmodelbase import ViewModelBase
from padawan.services import cms_service


class PublicationListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.publications = cms_service.all_publications()
