__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import time

import pyodbc


class LVSDispatcher:
    """
    Class to connect and work with data generated by an Omron Microscan LVS-95XX series of
    handheld barcode verifiers
    """
    def __init__(self, upper_read_index: int = 0):
        """

        :param upper_read_index: Will set the highest read index to track when new data is added to the LVS database
        """
        self.connection = None
        self.cursor = None
        self.upper_read_index = upper_read_index
        self.conn_string = ''

    def connect(self,
                host_server: str = None,
                user: str = None,
                password: str = None,
                database: str = None,
                port: int = 3306):
        """
        Method to establish connection to database. The default connection with no parameters will connect to the
        LVS software's default Microsoft Access database. All other databases will require the installation of an
        ODBC compatible driver for the desired database.

        :param host_server: The host name or IP address of the non-standard LVS database
        :param user: Username for authentication on the non-standard LVS database server
        :param password: Password for authentication on the non-standard LVS database server
        :param database: Database name on the non-standard LVS database
        :param port: Connection port on the non-standard LVS database
        """
        if host_server is None:
            self.conn_string = r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\Public\LVS-95XX\LVS-95XX.mdb;'
        else:
            assert user is not None
            assert password is not None
            assert database is not None
            self.conn_string = (
                f"DRIVER={{MariaDB ODBC 3.1 Driver}};"
                f"User={user};"
                f"Password={password};"
                f"Database={database};"
                f"Server={host_server};"
                f"Port={str(port)}")
        self.connection = pyodbc.connect(self.conn_string)
        self.cursor = self.connection.cursor()

    def record_count(self) -> int:
        """
        Get the number of LVS records in the database.

        :return: Number of records
        :rtype: int
        """
        try:
            self.connection.commit()
            self.cursor.execute(f'select count(*) from ReportData where Sequence=0')
            rows = self.cursor.fetchone()
            return rows[0]
        except pyodbc.ProgrammingError as error:
            print(f'Reports not accessible: {error}')

    def symbol_text(self, index: int):
        """
        Get the symbol text at a given database index

        :param int index:
        :return:The string read in this record
        :rtype: str
        """
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

    def overall_grade(self, index: int):
        """
        Get the overall grade at a given database index

        :param int index:
        :return:The overall grade in this record
        :rtype: str
        """
        try:
            self.cursor.execute(f'select * from ReportData where '
                                f'ReportID={str(index)} and ParameterName=\'Overall grade\'')
            row = self.cursor.fetchone()
            if row is None:
                return row
            else:
                return row[4]
        except pyodbc.ProgrammingError as error:
            print(f'Reports not accessible: {error}')

    def get_record(self, index: int):
        """
        Get the LVS record at a given database index

        :param int index:
        :return: The LVS record at the requested index
        """
        previous_length = 0
        try:

            self.cursor.execute(f'select * from ReportData where '
                                f'ReportID={str(index)}')
            record = self.cursor.fetchall()
            while len(record) != previous_length:
                previous_length = len(record)
                # Wait a bit and read again, as the LVS write takes time
                time.sleep(.1)
                self.connection.commit()
                self.cursor.execute(f'select * from ReportData where '
                                    f'ReportID={str(index)}')
                record = self.cursor.fetchall()
                # print(f'previous_length: {previous_length}, current_length = {len(record)}')

            self.upper_read_index = index
            return record
        except pyodbc.ProgrammingError as error:
            print(f'Reports not accessible: {error}')

    def get_previous_n_records(self, number_of_records: int, record_count: int = None):
        """
        Read multiple LVS records in reverse order. By default, it reads from the last recorded record.

        :param int number_of_records: Number of records to read with the final record being specified in record count
        :param record_count: The record index of the LVS record that will be the last in the list of records
        :return: List of LVS records
        """
        if record_count is None:
            record_count = self.record_count()
        record_read_index = record_count - number_of_records + 1
        record_list = []
        for index in range(number_of_records):
            record_list.append(self.get_record(record_read_index))
            record_read_index += 1
        return record_list

    def read_upper_records(self):
        """
        This method will read all records added since the last read. This is a helpful method for an event loop
        where the programmer needs to obtain records as the LVS reader places them in the database

        :return: List of LVS records since the last read
        """
        current_count = self.record_count()
        number_of_records = current_count - self.upper_read_index
        return self.get_previous_n_records(number_of_records, current_count)

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
