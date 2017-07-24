'''
Created on May 11, 2017

@author: Devin
'''

import json
import os
import psycopg2
import argparse

def _simple_sanitize(s):
    return s.split(';')[0]

def run(config, tablename, file_path, sql_file=None, range_col=None, range_start=None, range_end=None):
    if not file_path:
        file_path = tablename
    conn = psycopg2.connect(**config['db'])
    unload_options = '\n'.join(config.get('unload_options', []))
    cursor = conn.cursor()
    query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}' ORDER BY ordinal_position".format(tablename)
    cursor.execute(query)
    res = cursor.fetchall()

    cast_columns = []
    columns = [x[0] for x in res]
    for col in res:
        if 'boolean' in col[1]: # Boolean is a special case; cannot be casted to text so it needs to be handled differently
            cast_columns.append("CASE {} WHEN 1 THEN \\\'true\\\' ELSE \\\'false\\\'::text END".format(col[0]))
        else:
            cast_columns.append("{}::text".format(col[0]))

    header_str = ''
    for i in columns:
        header_str += "\\\'" + i + "\\\' as " + i.split(':')[0] + ', '
    header_str = header_str.rstrip().rstrip(',')
    column_str = ", ".join(columns)
    cast_columns_str = ", ".join(cast_columns)

    cursor = conn.cursor()
    where_clause = ""
    if range_col and range_start and range_end:
        where_clause = cursor.mogrify("WHERE %s BETWEEN %s AND %s", range_col, range_start, range_end)
    elif sql_file:
        where_clause = sql_file
    query = """
    UNLOAD (\'SELECT {0} FROM (
        SELECT 1 as i, {1} 
        UNION ALL
        (SELECT 2 as i, {2} 
        FROM {3} {4})) ORDER BY i\')  
    TO \'{7}\'
    CREDENTIALS 'aws_access_key_id={5};aws_secret_access_key={6}'
    {8}
    """.format(column_str, header_str, cast_columns_str, tablename, 
               where_clause, config['aws_access_key_id'], 
               config['aws_secret_access_key'], file_path, unload_options)
    print "The following UNLOAD query will be run: \n" + query
    confirmation = raw_input("\nContinue? (y/n)")
    if confirmation != 'y':
        print 'Exiting.'
    else:
        cursor.execute(query)
        print 'Completed write to {}'.format(file_path)

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.loads(f.read())

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Table name')
    parser.add_argument('-f', help='Desired S3 file path')
    parser.add_argument('-s', help='SQL WHERE clause')
    parser.add_argument('-r', help='Range column')
    parser.add_argument('-r1', help='Range start')
    parser.add_argument('-r2', help='Range end')
    raw_args = parser.parse_args() 
    if 's' in vars(raw_args):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), raw_args.s), 'r') as f:
            raw_args.s = f.read()
    args = {}
    for k, v in vars(raw_args).items():
        if v:
            args[k] = _simple_sanitize(v)
        else:
            args[k] = None
    run(config, args['t'], args['f'], args['s'], args['r'], args['r1'], args['r2'])