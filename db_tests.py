import mysql.connector
print(mysql.connector.__version__)
cnx = mysql.connector.connect(user='root', password='Charm1523_',
                              host='localhost', raise_on_warnings=True,
                              database='test')

print(cnx.is_connected())

db = cnx.cursor(buffer=True)
query = """SELECT * FROM permissions""" 
db.execute(query)
print(db.fetchall())
cnx.close()