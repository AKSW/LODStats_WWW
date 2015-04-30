import rdflib
import os
import codecs


voidDir = os.listdir('void')
length = len(voidDir)
for num, f in enumerate(voidDir):
    if(num < 4044):
        continue
    print f
    store = rdflib.Graph()
    print("Processing %s out of %s"%(str(num), str(length)))
    if(f.split('.')[-1] == 'ttl'):
        store.parse('./void/'+f, format='turtle')
    else:
        store.parse('./void/'+f, format='nt')
    store.serialize(format='nt')
