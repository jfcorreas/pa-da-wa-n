from padawan.viewmodels.shared.viewmodelbase import ViewModelBase
from padawan.services import search_service


class ResultsViewModel(ViewModelBase):
    def __init__(self, query_str: str):
        super().__init__()

        self.query_str = query_str
        self.num_results = None
        self.error = None
        self.results = None

        if self.query_str:
            self.results = search_service.search_publications(query_str)
            if self.results:
                self.num_results = len(self.results)
            else:
                self.error = "No results found"
        else:
            self.query_str = ''
