import csv
from sunlightapi.legislators.models import Committee, Legislator
from django.db.models import Q

lines = csv.reader(open('committees.csv'))
parent = None

problems = set()

for data in lines:
    coms = data[0].split('/')
    com_id = data[1]
    com = coms[-1]
    chamber = coms[0].split(' ')[0]
    if len(coms) == 1:
        parent = None
    committee = Committee.objects.create(id=com_id, chamber=chamber, parent=parent, name=com)
    if len(coms) == 1:
        parent = committee
    members = data[2:]
    for member in members:
        if member.strip():
            split = member.strip().split(' ')
            fname = split[0]
            lname = split[-1]
            if lname in ('Jr.','IV'):
                lname = split[-2]
            lname = lname.replace('_', ' ')

            # possible titles
            if chamber == 'Senate':
                titles = ['Sen']
            elif chamber == 'House':
                titles = ['Rep', 'Com', 'Del']
            else:
                titles = ['Rep', 'Sen', 'Com', 'Del']

            legislators = Legislator.objects.filter(lastname=lname, title__in=titles)

            # handle errors
            if len(legislators) == 0:
                problems.add('no legislator named %s _%s_ [%s,%s]' % (fname, lname, committee, committee.id))
            elif len(legislators) > 1:
                legislators = legislators.filter(Q(firstname=fname)|Q(nickname=fname))
                if len(legislators) == 0:
                    problems.add('no legislator named %s %s [%s,%s]' % (fname, lname, committee, committee.id))
                elif len(legislators) > 1:
                    problems.add('multiple legislators named %s %s [%s,%s]' % (fname, lname, committee, committee.id))
                else:
                    committee.members.add(legislators[0])
            else:
                committee.members.add(legislators[0])

additions = {'R000572': ('HSIF', 'HSIF_cti', 'HSIF_hth', 'HSIG'),
             'R000575': ('HSAG', 'HSAG_ene', 'HSAG_ldp', 'HSAS', 'HSAS_rdi', 'HSAS_osi', 'HSHM', 'HSHM_bor', 'HSHM_cpr'),
             'Y000031': ('HSAP', 'HSAP_def', 'HSAP_dva')}

for problem in problems:
    print problem

for bioguide_id, com_list in additions.iteritems():
    leg = Legislator.objects.get(pk=bioguide_id)
    for cname in com_list:
        c = Committee.objects.get(pk=cname)
        c.members.add(leg)
        print 'added %s to %s' % (leg, c)
