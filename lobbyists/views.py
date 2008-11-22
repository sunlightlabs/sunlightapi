import re
import string
from collections import defaultdict
from sunlightapi.lobbyists.models import Filing, Lobbyist, LobbyistBucket
from sunlightapi.api.utils import apimethod, APIError, score_match

@apimethod('lobbyists.getFiling')
def lobbyists_getfiling(params):
    """ Run a query against the Filings table based on params
    """
    id = params['id']
    filing = Filing.objects.get(pk=id)
    return filing.to_dict()

@apimethod('lobbyists.search')
def lobbyists_search(params):
    """ Attempt to match a Lobbyist based on their name
    
        * use initials to get a bucket
        * find via string matching algorithm and attempt to group by name
    """
    
    # handle name & threshold params
    name = re.sub('[^a-zA-Z ]', '', params['name'])
    name = string.capwords(name)
    # t=0.9 works much better for lobbyists
    threshold = float(params.get('threshold', 0.9))
    
    # get buckets from fingerprint
    fingerprint = re.sub('[^A-Z]', '', name)
    buckets = LobbyistBucket.objects.filter(bucket=fingerprint).select_related()
    if not buckets and len(fingerprint) > 1:
        buckets = LobbyistBucket.objects.filter(bucket=fingerprint[-1])
        name = name.rsplit(' ', 1)[-1]
        
    if buckets:
        # score names against uppercased name
        name = name.upper()
        # NOTE: this is not the final sort (as it is in the legislator sort)
        # but should still be valuable as it allows us to use a break in the
        # first for loop.
        scores = sorted([(score_match(name, bucket), bucket) for bucket in buckets], reverse=True)
        
        # store list of results and seen lobbyists
        lobbyists = defaultdict(list)
        
        # run a pass over scores, grouping by unique name/clientname
        for score, bucket in scores:
            # only turn lobbyists into results while score > threshold
            if score > threshold:
                
                # get lobbyist with client & filing_id
                lobbyist = bucket.person
                
                # check if this lobbyist name+client combo has been seen before
                unique_fields = (score, lobbyist.firstname, lobbyist.lastname,
                                 lobbyist.filing.client_name)
                lobbyists[unique_fields].append(lobbyist.filing_id)
            else:
                break

        # create result list from name,
        results = []
        for lobbyist, filings in lobbyists.iteritems():
            # split lobbyist into parts
            score, firstname, lastname, client_name = lobbyist
            result = {'result': {'score': lobbyist[0],
                                 'lobbyist': {'firstname': lobbyist[1],
                                              'lastname': lobbyist[2],
                                              'client_name': lobbyist[3],
                                              'filings': filings}}}
            results.append(result)
            
        # have to resort keys
        results.sort(key=lambda r: r['result']['score'], reverse=True)

        return {'results': results}
    else:
        return {'results': []}