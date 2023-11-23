

`pip install pyodbc`


```python
import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=path where you stored the Access file\file name.accdb;')
cursor = conn.cursor()
cursor.execute('select * from table_name')
   
for row in cursor.fetchall():
    print (row)
```
