from sunlightapi.legislators.models import Committee, Legislator
from django.db.models import Q

lines = open('committees.csv').readlines()
parent = None

problems = set()

for line in lines:
    data = line.split('","')
    coms = data[0].replace('"', '').split('/')
    com = coms[-1]
    chamber = coms[0].split(' ')[0]
    if len(coms) == 1:
        parent = None
    committee = Committee.objects.create(chamber=chamber, parent=parent, name=com)
    if len(coms) == 1:
        parent = committee
    members = data[1:]
    if members:
        members[-1] = members[-1].replace(',', '').replace('"','').strip()
    for member in members:
        if member.strip():
            split = member.strip().split(' ')
            fname = split[0]
            lname = split[-1]
            if lname in ('Jr.','IV'):
                lname = split[-2]
            lname = lname.replace('_', ' ')
            titles = ['Sen'] if chamber == 'Senate' else ['Rep', 'Com', 'Del']
            legislators = Legislator.objects.filter(lastname=lname, title__in=titles)
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

additions = {'R000572': (25,36,38,39,59),
             'R000575': (1,2,6,21,23,100,101,105),
             'Y000031': (11,18,8)}

for problem in problems:
    print problem

for bioguide_id, com_list in additions.iteritems():
    leg = Legislator.objects.get(pk=bioguide_id)
    for cname in com_list:
        c = Committee.objects.get(pk=cname)
        c.members.add(leg)
        print 'added %s to %s' % (leg, c)
