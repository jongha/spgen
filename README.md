# Stored Procedure Generator
[![Build Status](https://travis-ci.org/jongha/spgen.png?branch=master)](https://travis-ci.org/jongha/spgen)

spgen is Stored Procedure Generator for MySQL. It's a Python script. It auto generates Stored Procedure which includes add, update, delete functions from existing tables.

## Requirements

The program requires Python 2.x or Python 3.x.
You must install a [MySQL connector for python](http://dev.mysql.com/downloads/connector/python/).

## Usage

### From the command line

    usage: spgen.py [-h] [-P PORT] [-u USER] [-p PASSWORD] [-d] host database

    $ spgen.py -uim -ppw localhost mydb

    positional arguments:
        host                  Host to connect.
        database              Database name.

    optional arguments:
        -h, --help            show this help message and exit
        -P PORT, --port PORT  Port number to use for connection or 0 for default.
        -u USER, --user USER  User for login.
        -p PASSWORD, --password PASSWORD Password to use when connection to server.
        -d, --debug           Set Debug mode.


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

    spgen.build(debug=False) # debug argument is option
    spgen.close()

    exit(1)

except:
    exit(0)
```

## License

spgen is available under the terms of the MIT License.
