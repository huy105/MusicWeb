import pypyodbc

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

server = "GIAHUY-PC\SQLEXPRESS"  # Thay thế bằng tên máy chủ thực tế
database = "Test"  # Thay thế bằng tên cơ sở dữ liệu thực tế
connection_string = f"Driver={{SQL Server}};Server={server};Database={database}"
conn_sql_server = pypyodbc.connect(connection_string)

# cursor = conn_sql_server.cursor()
# cursor.execute("select * from users where username = 'giahuy105'")
# data = cursor.fetchall()[0]
# print(data)
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# password = "huy123456"
# plain_pass = pwd_context.hash(password)
# print(plain_pass)