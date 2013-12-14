#!/usr/bin/env python

from spgen.spgen import Spgen

spgen = Spgen()
spgen.connect(
    host = 'localhost',
    database = 'spgen_test',
    user = 'travis',
    password = None);

spgen.build()
spgen.close()

exit(1)
