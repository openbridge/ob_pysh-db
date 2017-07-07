'''
Created on May 11, 2017

@author: Devin
'''

import json
import psycopg2
import argparse
    
def run(config, tablename, date_start=None, date_end=None, file_path=None):
    if not file_path:
        file_path = tablename
    conn = psycopg2.connect(**config['db'])
    cursor = conn.cursor()
    query = "select column_name, data_type from information_schema.columns where table_name = '{}' order by ordinal_position".format(tablename)
    cursor.execute(query)
    res = cursor.fetchall()

    cast_columns = []    
    columns = [x[0] for x in res]
    for col in res:
        if 'boolean' in col[1]:
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
    date_query = ""
    if date_start and date_end:
        date_query = "WHERE date BETWEEN \\\'{}\\\' AND \\\'{}\\\'".format(date_start, date_end)
    query = """
    UNLOAD (\'SELECT {0} FROM (
        SELECT 1 as i, {1} 
        UNION ALL
        (SELECT 2 as i, {2} 
        FROM {3} {4})) ORDER BY i\')  
    TO \'{7}\'
    CREDENTIALS 'aws_access_key_id={5};aws_secret_access_key={6}'
    ADDQUOTES
    PARALLEL OFF
    ALLOWOVERWRITE
    DELIMITER ','
    GZIP
    """.format(column_str, header_str, cast_columns_str, tablename, date_query, config['aws_access_key_id'], config['aws_secret_access_key'], file_path)
    print "Running UNLOAD query: \n" + query
    cursor.execute(query)
    print 'Completed write to {}'.format(file_path)

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Table name')
    parser.add_argument('-f', help='Desired S3 file path')
    parser.add_argument('-d1', help='Date start')
    parser.add_argument('-d2', help='Date end')
    args = parser.parse_args()
    run(config, args.t, args.d1, args.d2, args.f)
