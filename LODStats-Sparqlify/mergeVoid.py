import rdflib
import os
import codecs

store = rdflib.Graph()

voidDir = os.listdir('void')
length = len(voidDir)
for num, f in enumerate(voidDir):
    print("Processing %s out of %s"%(str(num), str(length)))
    if(f.split('.')[-1] == 'ttl'):
        store.parse('./void/'+f, format='turtle')
    else:
        store.parse('./void/'+f, format='nt')

f = codecs.open('void-aggregated.nt', 'w', 'utf-8')
f.write(store.serialize(format='nt'))
f.close()
