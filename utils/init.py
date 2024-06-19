import pyodbc

server = 'lucks.database.windows.net'
database = 'TPI_medic'
username = 'lucadavid'
password = 'parola1234!'
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

