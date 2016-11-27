import re
import os

REPS_FILENAME = 'data/reps.csv'
STATSR_FILENAME = 'data/stats.csv'
POLITIKERE_FILENAME = 'data/politikere.csv'


def save(alist, filename):
    with open(filename, 'w', encoding='UTF-8') as out:
        for l in sorted(alist):
            print(l, file=out)


def find(name, reps):
    for rep in reps:
        rep_name, rep_parti = rep.split('|')
        if rep_name == name and 'none' != rep_parti:
            return rep_name, rep_parti
    return name, 'UNK'


def load_politikere():
    politikere = dict()
    if not os.path.isfile(POLITIKERE_FILENAME):
        with open("data/ordinary.csv", "r", encoding="UTF-8") as f:
            tmp_politikere = set()
            for line in f:
                segs = line.split('|')
                m = re.search('(?P<name>[\sa-zA-ZæøåÆØÅ.-]+)(?P<parti>\((.*)\))?', segs[3])
                if m != None:
                    name = m.group('name').strip()
                    parti = m.group('parti')
                    if parti != None:
                        parti = re.sub('[()]', '', parti)
                    if name == '':
                        continue
                    politiker = name + '|' + str(parti)
                    tmp_politikere.add(re.sub(' +', ' ', politiker.lower()))

            _reps = set()
            _stats = set()
            for p in sorted(tmp_politikere):
                p = p.replace('statstråd', 'statsråd').replace('statråd', 'statsråd')
                if 'statsråd' in p or 'statsminister' in p:
                    _stats.add(p)
                else:
                    _reps.add(p)

            # Clean up statsråder
            statsrader = set()
            for s in _stats:
                name, parti = s.split('|')
                if len(name.split()) < 2:
                    continue
                tmp = name.replace('statsråd', '').replace('statsminister', '').strip()
                rep_name, rep_parti = find(tmp, _reps)
                statsrader.add(rep_name + '|' + rep_parti)


            # Clean up stortingsrepresentanter
            representanter = set()
            for p in sorted(_reps):
                name, parti = p.split('|')
                if len(name.split()) < 2:
                    continue
                rep_name, rep_parti = find(name, _reps)
                representanter.add(rep_name + '|' + rep_parti)

        tmp_result = statsrader.union(representanter)
        save(representanter, REPS_FILENAME)
        save(statsrader, STATSR_FILENAME)
        save(tmp_result, POLITIKERE_FILENAME)

        for p in tmp_result:
            name, parti = p.split('|')
            politikere[name] = parti
    else:
        with open(POLITIKERE_FILENAME, 'r', encoding='UTF-8') as f:
            for p in f:
                name, parti = p.strip().split('|')
                politikere[name] = parti

    return politikere




if __name__ == '__main__':
    pol = load_politikere()

    for name in pol:
        print(name + ":" + pol[name])

    with open("data/ordinary.csv", "r", encoding="UTF-8") as f:
        tmp_politikere = set()
        for line in f:
            segs = line.split('|')
            m = re.search('(?P<name>[\sa-zA-ZæøåÆØÅ.-]+)(?P<parti>\((.*)\))?', segs[3])
            if m != None:
                tmp_name = m.group('name').strip().lower()
                position = 'representant'
                if tmp_name.startswith('statsråd'):
                    position = 'statsråd'
                elif tmp_name.startswith('statsminister'):
                    position = 'statsminister'

                name = tmp_name.replace('statsråd', '').replace('statsminister', '').strip()
                try:
                    print(name + '  -->  ' + pol[name].upper())
                except Exception as e:
                    print('Not found: ' + tmp_name)







