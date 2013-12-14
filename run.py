#!/usr/bin/env python

import spgen.spgen

spgen = Spgen()
spgen.connect(
    host = 'localhost',
    database = 'spgen_test',
    user = 'travis',
    password = None);

spgen.build();
spgen.close();

exit(1)
