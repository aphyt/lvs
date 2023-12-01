__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\Public\LVS-95XX\LVS-95XX.mdb;')
cursor = conn.cursor()
tables = cursor.tables()
table_list = []
for table in tables:

    table_list.append(table[2])

for table in table_list:
    print(f'Table is: {table}')
    try:
        cursor.execute(f'select * from {table}')
        # for row in cursor.fetchall():
        #     print(row)
    except pyodbc.ProgrammingError as error:
        print(f'{table} not accessible')

try:
    cursor.execute(f'select * from ReportData')
    columns = [column[0] for column in cursor.description]
    print(columns)
    # print(f'Number of reports is {len(cursor.fetchall())}')
    for row in cursor.fetchall():
        print(row)
except pyodbc.ProgrammingError as error:
    print(f'Reports not accessible')

cursor.close()
conn.close()
