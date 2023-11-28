__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import pyodbc


class LVSDispatcher:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, host_server: str, user: str, password: str, database: str, port: int = 3306):
        conn_string = (
            f"DRIVER={{MariaDB ODBC 3.1 Driver}};"
            f"User={user};"
            f"Password={password};"
            f"Database={database};"
            f"Server={host_server};"
            f"Port={str(port)};")
        self.connection = pyodbc.connect(conn_string)
        self.cursor = self.connection.cursor()

    def record_count(self):
        try:
            self.cursor.execute(f'select * from ReportData where Sequence=0')
            rows = self.cursor.fetchall()
            return len(rows)
        except pyodbc.ProgrammingError as error:
            print(f'Reports not accessible: {error}')

    def symbol_text(self, index: int):
        try:
            self.cursor.execute(f'select * from ReportData where '
                                f'ReportID={str(index)} and ParameterName=\'Decoded text\'')
            row = self.cursor.fetchone()
            if row is None:
                return row
            else:
                return row[4]
        except pyodbc.ProgrammingError as error:
            print(f'Reports not accessible: {error}')

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
