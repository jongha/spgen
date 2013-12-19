#!/usr/bin/env python

from spgen.spgen import Spgen

try:
    spgen = Spgen()
    spgen.connect(
        host = 'localhost',
        database = 'spgen_test',
        user = 'travis',
        password = None);
    
    spgen.build(debug=False)
    spgen.close()

    exit(1)

except:
    exit(0)
