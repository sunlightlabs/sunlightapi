import urllib
import cjson

class Namespace(object):
    def __init__(self, pvs):
        self._pvs = pvs

    def _apicall(self, func, params):
        return self._pvs._apicall(self.__class__.__name__ + '.' + func, params)

class Address(Namespace):

    def __init__(self, pvs):
        super(Address, self).__init__(pvs)

    def getCampaign(self, candidateId):
        return self._apicall('getCampaign', {'candidateId':candidateId})

    def getCampaignWebAddress(self, candidateId):
        return self._apicall('getCampaignWebAddress',
                             {'candidateId':candidateId})

    def getCampaignByElection(self, electionId):
        return self._apicall('getCampaignByElection', {'electionId':electionId})

    def getOffice(self, candidateId):
        return self._apicall('getOffice', {'candidateId':candidateId})

    def getOfficeWebAddress(self, candidateId):
        return self._apicall('getOfficeWebAddress', {'candidateId':candidateId})

    def getOfficeByOfficeState(self, officeId, stateId=None):
        return self._apicall('getOfficeByOfficeState',
                             {'officeId':officeId, 'stateId':stateId})

class CandidateBio(Namespace):
    def getBio(self, candidateId):
        return self._apicall('getBio', {'candidateId':candidateId})

    def getaddlBio(self, candidateId):
        return self._apicall('getaddlBio', {'candidateId':candidateId})

class Candidates(Namespace):
    def getByOfficeState(self, officeId, stateId=None, electionYear=None):
        params = {'officeId':officeId}
        if stateId:
            params['stateId'] = stateId
        if electionYear:
            params['electionYear'] = electionYear
        return self._apicall('getByOfficeState', params)

    def getByLastname(self, lastName, electionYear=None):
        params = {'lastName':lastName}
        if electionYear:
            params['electionYear'] = electionYear
        return self._apicall('getByLastname', params)

    def getByLevenstein(self, lastName, electionYear=None):
        params = {'lastName':lastName}
        if electionYear:
            params['electionYear'] = electionYear
        return self._apicall('getByLevenstein', params)

    def getByElection(self, electionId):
        return self._apicall('getByElection', {'electionId': electionId})

    def getByDistrict(self, districtId, electionYear=None):
        params = {'districtId':districtId}
        if electionYear:
            params['electionYear'] = electionYear
        return self._apicall('getByDistrict', params)

class Committee(Namespace):
    def getTypes(self):
        return self._apicall('getTypes', None)

    def getCommitteesByTypeState(self, typeId=None, stateId=None):
        params = {}
        if typeId:
            params['typeId'] = typeId
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getCommitteesByTypeState', params)

    def getCommittee(self, committeeId):
        return self._apicall('getCommittee', {'committeeId' : committeeId})

    def getCommitteeMembers(self, committeeId):
        return self._apicall('getCommitteeMembers',
                             {'committeeId' : committeeId})

class District(Namespace):
    def getByOfficeState(self, officeId, stateId, districtName=None):
        params = {'officeId':officeId, 'stateId':stateId}
        if districtName:
            params['districtName'] = districtName
        return self._apicall('getByOfficeState', params)

class Election(Namespace):
    def getElection(self, electionId):
        return self._apicall('getElection', {'electionId':electionId})

    def getElectionByYearState(self, year, stateId):
        return self._apicall('getElectionByYearState',
                             {'year':year, 'stateId':stateId})

    def getStageCandidates(self, electionId, stageId, party=None, districtId=None):
        params = {'electionId':electionId, 'stageId':stageId}
        if party:
            params['party'] = party
        if districtId:
            params['districtId'] = districtId
        return self._apicall('getStageCandidates', params)

class Leadership(Namespace):
    def getPositions(self, stateId=None, officeId=None):
        params = {}
        if stateId:
            params['stateId'] = stateId
        if officeId:
            params['officeId'] = officeId
        return self._apicall('getPositions', params)

    def getCandidates(self, leadershipId, stateId=None):
        params['leadershipId'] = leadershipId
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getCandidates', params)

class Local(Namespace):
    def getCounties(self, stateId):
        return self._apicall('getCounties', {'stateId':stateId})

    def getCities(self, stateId):
        return self._apicall('getCities', {'stateId':stateId})

    def getOfficials(self, localId):
        return self._apicall('getOfficials', {'localId':localId})

class Measure(Namespace):
    def getMeasuresByYearState(self, year, stateId):
        return self._apicall('getMeasuresByYearState',
                             {'year':year, 'stateId':stateId})

    def getMeasure(self, measureId):
        return self._apicall('getMeasure', {'measureId':measureId})

class Npat(Namespace):
    def getNpat(self, candidateId):
        return self._apicall('getNpat', {'candidateId': candidateId})

class Office(Namespace):
    def getTypes(self):
        return self._apicall('getTypes', {})

    def getBranches(self):
        return self._apicall('getBranches', {})

    def getLevels(self):
        return self._apicall('getLevels', {})

    def getOfficesByType(self, typeId):
        return self._apicall('getOfficesByType', {'typeId': typeId})

    def getOfficesByLevel(self, levelId):
        return self._apicall('getOfficesByLevel', {'typeId': typeId})

    def getOfficesByTypeLevel(self, typeId, levelId):
        return self._apicall('getOfficesByTypeLevel',
                             {'typeId': typeId, 'levelId': levelId})

    def getOfficesByBranchLevel(self, branchId, levelId):
        return self._apicall('getOfficesByBranchLevel',
                             {'branchId': branchId, 'levelId': levelId})

class Officials(Namespace):
    def getByOfficeState(self, officeId, stateId=None):
        params = {'officeId': officeId}
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getByOfficeState', params)

    def getByLastname(self, lastName):
        return self._apicall('getByLastname', {'lastName': lastName})

    def getByLevenstein(self, lastName):
        return self._apicall('getByLevenstein', {'lastName': lastName})

    def getByElection(self, electionId):
        return self._apicall('getByElection', {'electionId': electionId})

    def getByDistrict(self, districtId):
        return self._apicall('getByDistrict', {'districtId': districtId})

class Rating(Namespace):
    def getCategories(self, stateId=None):
        params = {}
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getCategories', params)

    def getSigList(self, categoryId, stateId):
        return self._apicall('getSigList',
                             {'categoryId': categoryId,
                              'stateId': stateId})

    def getSig(self, sigId):
        return self._apicall('getSig', {'sigId': sigId})

    def getCandidateRating(self, candidateId, sigId):
        return self._apicall('getCandidateRating',
                             {'candidateId': candidateId,
                              'sigId': sigId})

class State(Namespace):
    def getStateIDs(self):
        return self._apicall('getStateIDs', {})

    def getState(self, stateId):
        return self._apicall('getState', {})

class Votes(Namespace):
    def getCategories(self, year, stateId=None):
        params = {'year': year}
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getCategories', params)

    def getBill(self, billId):
        return self._apicall('getBill', {'billId': billId})

    def getBillAction(self, actId):
        return self._apicall('getBillAction', {'actId': actId})

    def getBillActionVotes(self, actId):
        return self._apicall('getBillActionVotes', {'actId': actId})

    def getBillActionVoteByCandidate(self, actId, candidateId):
        return self._apicall('getBillActionVoteByCandidate',
                             {'actId': actId,
                              'candidateId': candidateId})

    def getBillsByCategoryYearState(self, categoryId, year, stateId=None):
        params = {'categoryId': categoryId, 'year': year}
        if stateId:
            params['stateId'] = stateId
        return self._apicall('getBillsByCategoryYearState', params)

    def getBillsByYearState(self, year, stateId):
        return self._apicall('getBillsByYearState',
                             {'year': year, 'stateId': stateId})

    def getBillsByOfficialYearOffice(self, candidateId, year, officeId=None):
        params = {'candidateId': candidateId, 'year': year}
        if officeId:
            params['officeId'] = officeId
        return self._apicall('getBillsByOfficialYearOffice', params)

    def getBillsByCandidateCategoryOffice(self, candidateId, categoryId,
                                          officeId=None):
        params = {'candidateId': candidateId, 'categoryId': categoryId}
        if officeId:
            params['officeId'] = officeId
        return self._apicall('getBillsByCandidateCategoryOffice', params)

    def getBillsBySponsorYear(self, candidateId, year):
        return self._apicall('getBillsBySponsorYear',
                             {'candidateId': candidateId,
                              'year': year})

    def getBillsBySponsorCategory(self, candidateId, categoryId):
        return self._apicall('getBillsBySponsorCategory',
                             {'candidateId': candidateId,
                              'categoryId': categoryId})

class VoteSmart(object):

    API_SERVER = 'http://api.votesmart.org/%s?%s'

    def __init__(self, key):
        self.baseurl = self.API_SERVER + '&key=%s&o=JSON' % key
        self.Address = Address(self)
        self.CandidateBio = CandidateBio(self)
        self.Candidates = Candidates(self)
        self.Committee = Committee(self)
        self.District = District(self)
        self.Election = Election(self)
        self.Leadership = Leadership(self)
        self.Local = Local(self)
        self.Measure = Measure(self)
        self.Npat = Npat(self)
        self.Office = Office(self)
        self.Officials = Officials(self)
        self.Rating = Rating(self)
        self.State = State(self)
        self.Votes = Votes(self)

    def _apicall(self, func, params):
        url = self.baseurl % (func, urllib.urlencode(params))
        json = urllib.urlopen(url).read()
        try:
            return cjson.decode(json)
        except cjson.DecodeError:
            print url,json
            raise
