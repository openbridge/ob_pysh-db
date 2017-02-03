'''
Created on Feb 3, 2017

@author: Devin
'''
import argparse
import psycopg2

def main(host, port, user, password, database):
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT table_name FROM information_schema.tables WHERE table_schema = '{}'".format(database))
    results = cursor.fetchall()
    for row in results:
        print row[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', action='store')
    parser.add_argument('-p', action='store', type=int)
    parser.add_argument('-u', action='store')
    parser.add_argument('-x', action='store')
    parser.add_argument('-d', action='store')
    args = parser.parse_args()
    main(args.h, args.p, args.u, args.x, args.d)