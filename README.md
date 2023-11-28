# Setup System
## Install Requirements
`pip install -r requirements.txt`
## Install MariaDB Connector
Should match the Python interpreter on 32-bit or 64-bit. The Microscan Access Database is 32-bit, so most development uses 32-bit connectors.

# Example with Microsoft Access Database
```python
import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=path where you stored the Access file\file name.accdb;')
cursor = conn.cursor()
cursor.execute('select * from table_name')
   
for row in cursor.fetchall():
    print (row)
```
