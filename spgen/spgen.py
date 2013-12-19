#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import os
import re
import time
import mysql.connector
from mysql.connector import errorcode

try:
    import argparse
except ImportError:
    from optparse import OptionParser

PROCEDURE_DROP_TEMPLATE = 'DROP PROCEDURE IF EXISTS `%(name)s`;'
PROCEDURE_CREATE_TEMPLATE = '''
CREATE PROCEDURE `%(name)s`(
%(param)s
)
BEGIN
    %(body)s
END
'''

class Spgen(object):
    cnx = None
    tables = []

    def __init__(self):
        return

    def close(self):
        print('Connection Closing...');
        if self.cnx is not None:
            self.cnx.close()

    def create(self, mode, table, columns):
        if mode == 'add':
            selected = []
            for c in columns:
                if c[5] != 'auto_increment' and c[1] != 'timestamp':
                    selected.append(c)

            return PROCEDURE_CREATE_TEMPLATE % {
                'name': mode + table,
                'param': ',\n'.join(map(lambda x: 'p_%s %s' % (x[0], x[1]), selected)),
                'body': 'insert into %s(%s) values(%s);' % (
                    table,
                    ', '.join(map(lambda x: x[0], selected)),
                    ', '.join(map(lambda x: 'p_%s' % (x[0]), selected))
                    )
                };

        elif mode == 'update':
            key_columns = []
            none_key_columns = []

            for c in columns:
                if c[3] in ('PRI', 'MUL'):
                    key_columns.append(c)
                else:
                    none_key_columns.append(c)

            if len(key_columns) == 0:
                return None;

            return PROCEDURE_CREATE_TEMPLATE % {
                'name': mode + table,
                'param': ',\n'.join(map(lambda x: 'p_%s %s' % (x[0], x[1]), columns)),
                'body': 'update %s set %s where %s;' % (
                    table,
                    ', '.join(map(lambda x: '%(name)s = p_%(name)s' % { 'name': x[0] }, none_key_columns)),
                    ' and '.join(map(lambda x: '%(name)s = p_%(name)s' % { 'name': x[0] }, key_columns))
                    )
                };

        elif mode == 'delete':
            key_columns = []
            for c in columns:
                if c[3] == 'PRI':
                    key_columns.append(c)

            if len(key_columns) == 0:
                return None;

            return PROCEDURE_CREATE_TEMPLATE % {
                'name': mode + table,
                'param': ',\n'.join(map(lambda x: 'p_%s %s' % (x[0], x[1]), key_columns)),
                'body': 'delete from %s where %s;' % (
                    table,
                    ' and '.join(map(lambda x: '%(name)s = p_%(name)s' % { 'name': x[0] }, key_columns))
                    )
                };

    def build(self, debug=False):
        cursor = self.cnx.cursor()
        cursor.execute('show tables')
        for data in cursor:
            self.tables.append(data[0])

        modes = ('add', 'update', 'delete')

        count = 0
        total = len(self.tables) * len(modes)
        for table in self.tables:
            cursor.execute('desc ' + table)

            columns = []
            for data in cursor:
                columns.append(data);

            for mode in modes:
                script = self.create(mode, table, columns)
                if script is not None:
                    drop_script = PROCEDURE_DROP_TEMPLATE % { 'name': mode + table }

                    cursor.execute(drop_script)
                    cursor.execute(script)

                    if debug: # show script for debug
                        print('\n')
                        print(drop_script)
                        print(script)

                count += 1
                sys.stdout.write('\rCreating... %d%%' % int(float(count) / float(total) * 100))
                sys.stdout.flush()

        sys.stdout.write('\n')
        sys.stdout.flush()

        print('Almost Done.')
        cursor.close()

    def connect(self, host, database, port=3306, user=None, password=None):
        print('Connection Opening... (%s@%s:%s/%s)' % (user, host, port, database));
        try:
            self.cnx = mysql.connector.connect(
                user=user,
                password=password,
                port=port,
                host=host,
                database=database)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password.')

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists.')

            else:
                print(err)

            exit(0);

if __name__ == '__main__':
    l_argv = len(sys.argv)
    parser = argparse.ArgumentParser(description='Stored Procedure Generator for MySQL.')
    parser.add_argument('host', metavar='host', nargs=1, help='Host to connect.')
    parser.add_argument('database', metavar='database', nargs=1, help='Database name.')
    parser.add_argument('-P', '--port', default=3306, help='Port number to use for connection or 0 for default.')
    parser.add_argument('-u', '--user', help='User for login.')
    parser.add_argument('-p', '--password', help='Password to use when connection to server.')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='Set Debug mode.')
    args = parser.parse_args()

    if l_argv > 1:
        spgen = Spgen()
        spgen.connect(
            host = args.host[0],
            database = args.database[0],
            port = args.port,
            user = args.user,
            password = args.password)

        spgen.build(debug=args.debug)
        spgen.close()
        print('Done.')
    else:
        print(args.accumulate(args.integers))