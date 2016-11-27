import re

DATASET_FILNAME = 'data/dataset.csv'

def dataset(parti=None):
    class MySentences(object):
        def __iter__(self):
            with open(DATASET_FILNAME, 'r', encoding='UTF-8') as f:
                for l in f:
                    segs = l.split('|')
                    if None != parti and parti == segs[3]:
                        tmp = re.sub('[^\sa-zA-Z0-9æøå]+', '', segs[4].lower())
                        tmp = re.sub('[,.?–]', ' ', tmp)
                        yield tmp.split()
                    elif None == parti:
                        tmp = re.sub('[^\sa-zA-Z0-9æøå]+', '', segs[4].lower())
                        tmp = re.sub('[,.?–]', ' ', tmp)
                        yield tmp.split()

    return MySentences()



if __name__ == '__main__':
    sent = dataset('h')
    print(sent)