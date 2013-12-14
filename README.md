# Stored Procedure Generator
[![Build Status](https://travis-ci.org/jongha/spgen.png?branch=master)](https://travis-ci.org/jongha/spgen)

spgen is Stored Procedure Generator for MySQL. It's a Python script. It auto generates Stored Procedure which includes add, update, delete functions from existing tables.

## Requirements

The program requires Python 2.x or Python 3.x.
You must install a [MySQL connector for python](http://dev.mysql.com/downloads/connector/python/).

## Usage

### From the command line

    usage: spgen.py [-h] [-P PORT] [-u USER] [-p PASSWORD] host database

    $ spgen.py -uim -ppw localhost mydb

### Using a Library

Check out the run.py file.

```
from spgen.spgen import Spgen

try:
    spgen = Spgen()
    spgen.connect(
        host = 'IP address',
        database = 'database name',
        port = 3306,
        user = 'user name',
        password = 'user password');

    spgen.build()
    spgen.close()

    exit(1)

except:
    exit(0)
```

## License

spgen is available under the terms of the MIT License.
