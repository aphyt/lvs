__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import mariadb
import sys
import pyodbc
# Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="LVS-95XX",
#         password="LVS-95XX",
#         host="192.168.250.115",
#         port=3306,
#         database="LVS-95XX"
#
#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
conn_string = ("DRIVER={MariaDB ODBC 3.1 Driver};User=LVS-95XX;Password=LVS-95XX;Database=LVS-95XX;Server=192.168.250.115;Port=3306;")
conn = pyodbc.connect(conn_string)
# conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\Public\LVS-95XX\LVS-95XX.mdb;')
# conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\Public\LVS-95XX\LVS-95XX.mdb;')
cursor = conn.cursor()
# tables = cursor.tables()
# table_list = []
# for table in tables:
#
#     table_list.append(table[2])

# for table in table_list:
#     print(f'Table is: {table}')
#     try:
#         cursor.execute(f'select * from {table}')
#         # for row in cursor.fetchall():
#         #     print(row)
#     except pyodbc.ProgrammingError as error:
#         print(f'{table} not accessible')

try:
    cursor.execute(f'select * from ReportData where Sequence=0')
    # columns = [column[0] for column in cursor.description]
    # print(columns)
    # print(f'Number of reports is {len(cursor.fetchall())}')
    rows = cursor.fetchall()
    print(len(rows))
    for row in rows:
        print(row)
except pyodbc.ProgrammingError as error:
    print(f'Reports not accessible')

cursor.close()
conn.close()
