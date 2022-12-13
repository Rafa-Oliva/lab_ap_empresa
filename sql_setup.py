import mysql.connector

dbconfig = { 'host': '127.0.0.1',
            'user': 'root',
            'password': 'teleco03',
            'database': 'search_log', }


conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()

_SQL = """show tables"""
cursor.execute(_SQL)

res = cursor.fetchall()
print(res)



