from sunlightapi.api.utils import apimethod, APIError
from sunlightapi.api.lobbyists.models import Lobbyist, Filing

    
@apimethod('lobbyists.getFiling')
def lobbyists_getfiling(params):
    """ Run a query against the Filings table based on params
    """
    id = params['id']
    filing = Filings.objects.get(pk=id)
    return filing.get_dict()

@apimethod('lobbyists.searchLobbyists')
def lobbyists_search(params):
    """ Attempt to match a Lobbyist based on their name"""