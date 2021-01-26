import logbook
from flask import Blueprint, request

from padawan.infraestructure.view_modifiers import response
from padawan.viewmodels.search.results_viewmodel import ResultsViewModel

blueprint = Blueprint('search', __name__, template_folder='templates')
log = logbook.Logger('search')


@blueprint.route('/search')
@response(template_file='search/results.html')
def search_page():
    query_str = request.args.get('query')
    vm = ResultsViewModel(query_str)
    log.info(f"Searching for: {query_str}")
    return vm.to_dict()

