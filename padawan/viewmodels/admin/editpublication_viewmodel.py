from padawan.services import cms_service
from padawan.viewmodels.shared.viewmodelbase import ViewModelBase


class EditPublicationViewModel(ViewModelBase):
    def __init__(self, publication_id: int = 0):
        super().__init__()

        self.title = ''
        self.short_url = ''
        self.content = ''
        self.preview = ''
        self.is_snippet = False
        self.publication = None
        self.publication_id = publication_id

        if self.publication_id:
            self.publication = cms_service.find_publication_by_id(self.publication_id)

        if self.publication:
            self.title = self.publication.title
            self.content = self.publication.content
            self.preview = self.publication.preview
            self.short_url = self.publication.short_url
            self.is_snippet = self.publication.is_snippet

        self.error = None

    def process_form(self):
        d = self.request_dict
        self.title = d.get('title', '').strip()
        self.content = d.get('contents', '').strip()
        self.short_url = d.get('short_url', '').strip().lower()
        self.is_snippet = (d.get('is_snippet', '') == 'on')

    def validate(self) -> bool:
        if not self.title or not self.title.strip():
            self.error = 'You must specify a title'
            return False

        if not self.content or not self.content.strip():
            self.error = 'You must specify the HTML content'
            return False

        if self.publication_id and not self.publication:
            self.error = f"The publication with ID {self.publication_id} doesn't exists"
            return False

        if self.short_url:
            other_publication = cms_service.get_publication_by_url(self.short_url)
            if other_publication and (other_publication.id != self.publication_id):
                self.error = f"The short url: /{self.short_url} already assigned to another publication"
                return False

        return True
