import pandas as pd
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pyodbc

driver = 'SQL Server'
server = 'DESKTOP-U1A9UJ9'
database = 'Contoso10M'

connection_string = f"""Driver={{SQL Server}};
                      Server={server};
                      Database={database};
                      "Trusted_Connection=yes;"""


connection_url = URL.create("mssql+pyodbc", query = {"odbc_connect": connection_string})
engine = create_engine(connection_url, module = pyodbc)

sql_query = "SELECT * FROM Data.Customer"

df = pd.read_sql_query(sql_query, engine)
print(df)